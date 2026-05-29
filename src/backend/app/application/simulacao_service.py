"""Orquestração da simulação — pipeline APIs + motor de cálculo."""

import logging
import uuid
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.application.calculo_simulacao import (
    calcular_dimensionamento,
    formatar_payback,
    projetar_25_anos,
)
from app.config import get_settings
from app.domain.calculo import EntradaCalculo
from app.domain.enums import (
    OrientacaoTelhado,
    StatusSimulacao,
    TipoConexao,
    TipoEntradaConsumo,
)
from app.domain.exceptions import DomainError, EntityNotFoundError
from app.infrastructure.db.models import (
    DadosConsumo,
    DadosTelhado,
    Localizacao,
    ProjecaoAnual,
    Resultado,
    Simulacao,
    Usuario,
)
from app.infrastructure.http.schemas import SimulacaoCreate

logger = logging.getLogger(__name__)
_settings = get_settings()

# Tarifas médias residenciais por UF (R$/kWh) — referência 2025/2026
TARIFAS_ESTADUAIS: dict[str, Decimal] = {
    "AC": Decimal("0.78"),
    "AL": Decimal("0.89"),
    "AP": Decimal("0.91"),
    "AM": Decimal("0.82"),
    "BA": Decimal("0.92"),
    "CE": Decimal("0.88"),
    "DF": Decimal("0.79"),
    "ES": Decimal("0.98"),
    "GO": Decimal("0.84"),
    "MA": Decimal("0.90"),
    "MT": Decimal("0.86"),
    "MS": Decimal("0.85"),
    "MG": Decimal("0.95"),
    "PA": Decimal("0.87"),
    "PB": Decimal("0.91"),
    "PR": Decimal("0.81"),
    "PE": Decimal("0.93"),
    "PI": Decimal("0.94"),
    "RJ": Decimal("1.05"),
    "RN": Decimal("0.90"),
    "RS": Decimal("0.88"),
    "RO": Decimal("0.84"),
    "RR": Decimal("0.88"),
    "SC": Decimal("0.82"),
    "SP": Decimal("0.83"),
    "SE": Decimal("0.96"),
    "TO": Decimal("0.87"),
}
TARIFA_FALLBACK = Decimal("0.85")
HSP_FALLBACK = Decimal("4.5")
MARCAS_FALLBACK = "Intelbras, WEG, Canadian Solar"

# Micro-etapa A — mocks para `executar_calculo_mock` (testes / compatibilidade)
TARIFA_MOCK = Decimal("0.83")
HSP_MOCK = Decimal("4.5")
EFICIENCIA_MOCK = Decimal("0.75")
CUSTO_POR_KWP_MOCK = Decimal("3800")
KWH_TAXA_MINIMA_MOCK = Decimal("50")
DIAS_MES_MOCK = Decimal("30")


def tarifa_por_uf(estado: str | None) -> Decimal:
    """Retorna tarifa média do estado ou fallback nacional."""
    if not estado:
        return TARIFA_FALLBACK
    return TARIFAS_ESTADUAIS.get(estado.upper().strip(), TARIFA_FALLBACK)


async def buscar_cep_brasil_api(cep: str) -> tuple[Decimal, Decimal, str, str]:
    """
    GET Brasil API v2 — extrai latitude, longitude, UF e cidade.
    Raises em falha de rede ou payload inválido.
    """
    cep_limpo = "".join(c for c in cep if c.isdigit())
    url = f"https://brasilapi.com.br/api/cep/v2/{cep_limpo}"
    async with httpx.AsyncClient(timeout=_settings.external_api_timeout_seconds) as client:
        response = await client.get(url)
        response.raise_for_status()
        payload = response.json()

    location = payload.get("location") or {}
    coordinates = location.get("coordinates") or {}
    lat_raw = coordinates.get("latitude")
    lon_raw = coordinates.get("longitude")
    if lat_raw is None or lon_raw is None:
        logger.warning(
            "Brasil API: CEP %s sem coordenadas (location.coordinates ausente ou incompleto)",
            cep_limpo,
        )
        raise ValueError("Coordenadas não disponíveis para o CEP informado")

    latitude = Decimal(str(lat_raw))
    longitude = Decimal(str(lon_raw))
    estado = str(payload.get("state") or "").upper()
    if not estado:
        raise ValueError("Estado (UF) não retornado pela Brasil API")
    cidade = str(payload.get("city") or payload.get("cidade") or "")
    return latitude, longitude, estado, cidade


async def buscar_hsp_nasa_power(latitude: Decimal, longitude: Decimal) -> Decimal:
    """
    GET NASA POWER climatology — média anual ALLSKY_SFC_SW_DWN (kWh/m²/dia).
    """
    url = (
        "https://power.larc.nasa.gov/api/temporal/climatology/point"
        f"?parameters=ALLSKY_SFC_SW_DWN&community=RE"
        f"&longitude={longitude}&latitude={latitude}&format=JSON"
    )
    async with httpx.AsyncClient(timeout=_settings.external_api_timeout_seconds) as client:
        response = await client.get(url)
        response.raise_for_status()
        payload = response.json()

    hsp_valor = payload["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]["ANN"]
    hsp = Decimal(str(hsp_valor)).quantize(Decimal("0.01"))
    if hsp <= 0:
        raise ValueError("HSP inválido retornado pela NASA POWER")
    return hsp


async def recomendar_equipamentos_gemini(
    potencia_kwp: Decimal, estado: str
) -> str:
    """Recomenda equipamentos via REST da API Gemini."""
    if not _settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY não configurada")

    prompt = (
        f"Atuando como um especialista em energia solar, recomende brevemente "
        f"2 marcas premium de painéis solares e 2 de inversores ideais para um "
        f"sistema de {potencia_kwp} kWp no estado de {estado}. "
        f"Retorne apenas texto direto, sem formatação markdown pesada, "
        f"em no máximo 2 linhas."
    )
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-1.5-flash:generateContent?key={_settings.gemini_api_key}"
    )
    async with httpx.AsyncClient(timeout=_settings.external_api_timeout_seconds) as client:
        response = await client.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        response.raise_for_status()
        payload = response.json()

    texto = payload["candidates"][0]["content"]["parts"][0]["text"].strip()
    if not texto:
        raise ValueError("Resposta vazia da Gemini API")
    return texto


@dataclass
class ResultadoCalculoMock:
    consumo_kwh: Decimal
    potencia_kwp: Decimal
    investimento: Decimal
    economia_mensal: Decimal
    payback_anos: Decimal


def calcular_com_mocks(
    *,
    valor_reais: Decimal | None,
    consumo_kwh: Decimal | None,
) -> ResultadoCalculoMock:
    """
    Motor simplificado (Micro-etapa A): física e financeiro com tarifa/HSP fixos.
    """
    if valor_reais and valor_reais > 0:
        gasto = valor_reais
        consumo = (gasto / TARIFA_MOCK).quantize(Decimal("0.01"))
    elif consumo_kwh and consumo_kwh > 0:
        consumo = consumo_kwh
        gasto = (consumo * TARIFA_MOCK).quantize(Decimal("0.01"))
    else:
        raise DomainError("Informe consumo em kWh ou valor em reais (RB01).")

    potencia = (
        (consumo / DIAS_MES_MOCK) / (HSP_MOCK * EFICIENCIA_MOCK)
    ).quantize(Decimal("0.01"))
    investimento = (potencia * CUSTO_POR_KWP_MOCK).quantize(Decimal("0.01"))
    economia_mensal = (
        gasto - (KWH_TAXA_MINIMA_MOCK * TARIFA_MOCK)
    ).quantize(Decimal("0.01"))

    if economia_mensal <= 0:
        raise DomainError(
            "Economia mensal insuficiente para calcular payback com os dados informados."
        )

    payback = (investimento / (economia_mensal * Decimal("12"))).quantize(
        Decimal("0.01")
    )

    return ResultadoCalculoMock(
        consumo_kwh=consumo,
        potencia_kwp=potencia,
        investimento=investimento,
        economia_mensal=economia_mensal,
        payback_anos=payback,
    )


def _decompor_payback(payback_anos: Decimal) -> tuple[int, int]:
    """Converte payback decimal (anos) em anos e meses inteiros para o banco."""
    meses_totais = int(
        (payback_anos * Decimal("12")).to_integral_value(rounding=ROUND_HALF_UP)
    )
    return meses_totais // 12, meses_totais % 12


@dataclass
class SimulacaoExecutada:
    simulacao: Simulacao
    payback_texto: str


class SimulacaoService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def criar_rascunho(self, usuario: Usuario, dados: SimulacaoCreate) -> Simulacao:
        if dados.consumo_kwh is None and dados.valor_reais is None:
            raise DomainError("Informe consumo em kWh ou valor em reais (RB01).")

        try:
            tipo_entrada = TipoEntradaConsumo(dados.tipo_entrada.upper())
            orientacao = OrientacaoTelhado(dados.orientacao.upper())
            tipo_conexao = TipoConexao(dados.tipo_conexao.upper())
        except ValueError as exc:
            raise DomainError("Enum de entrada inválido.") from exc

        sim = Simulacao(usuario_id=usuario.id, status=StatusSimulacao.INICIADA)
        self._db.add(sim)
        self._db.flush()

        self._db.add(
            DadosConsumo(
                simulacao_id=sim.id,
                consumo_kwh=dados.consumo_kwh,
                valor_reais=dados.valor_reais,
                tipo_entrada=tipo_entrada,
            )
        )
        self._db.add(
            Localizacao(
                simulacao_id=sim.id,
                cep=dados.cep,
                cidade=dados.cidade,
            )
        )
        self._db.add(
            DadosTelhado(
                simulacao_id=sim.id,
                area_m2=dados.area_m2,
                orientacao=orientacao,
                tipo_conexao=tipo_conexao,
            )
        )
        self._db.commit()
        self._db.refresh(sim)
        return sim

    def listar_do_usuario(self, usuario_id: uuid.UUID) -> list[Simulacao]:
        stmt = (
            select(Simulacao)
            .where(Simulacao.usuario_id == usuario_id)
            .order_by(Simulacao.realizada_em.desc())
        )
        return list(self._db.scalars(stmt).all())

    def obter(self, usuario_id: uuid.UUID, simulacao_id: uuid.UUID) -> Simulacao:
        sim = self._carregar_simulacao(simulacao_id)
        if not sim or sim.usuario_id != usuario_id:
            raise EntityNotFoundError("Simulação não encontrada.")
        return sim

    def executar_calculo_mock(
        self, usuario_id: uuid.UUID, simulacao_id: uuid.UUID
    ) -> Simulacao:
        """
        Micro-etapa B: calcula com mocks, persiste em `resultados` e marca CONCLUIDA.
        """
        sim = self.obter(usuario_id, simulacao_id)

        if sim.status == StatusSimulacao.CONCLUIDA and sim.resultado:
            return sim

        consumo = sim.dados_consumo
        if not consumo:
            raise DomainError("Simulação incompleta. Crie um rascunho válido primeiro.")

        calculo = calcular_com_mocks(
            valor_reais=consumo.valor_reais,
            consumo_kwh=consumo.consumo_kwh,
        )
        self._persistir_resultado_mock(sim, consumo, calculo)
        self._db.commit()
        return self.obter(usuario_id, simulacao_id)

    def _persistir_resultado_mock(
        self,
        sim: Simulacao,
        consumo: DadosConsumo,
        calculo: ResultadoCalculoMock,
    ) -> None:
        """Mapeia o resultado do motor mock para as tabelas ORM (models.py)."""
        if consumo.valor_reais and (
            consumo.tipo_entrada == TipoEntradaConsumo.REAIS or not consumo.consumo_kwh
        ):
            consumo.consumo_kwh = calculo.consumo_kwh

        loc = sim.localizacao
        if loc:
            loc.hsp = HSP_MOCK
            loc.tarifa_kwh = TARIFA_MOCK

        if sim.resultado:
            for proj in list(sim.resultado.projecoes):
                self._db.delete(proj)
            self._db.delete(sim.resultado)
            self._db.flush()

        payback_anos_int, payback_meses_int = _decompor_payback(calculo.payback_anos)
        geracao_kwh = (
            calculo.potencia_kwp * HSP_MOCK * DIAS_MES_MOCK * EFICIENCIA_MOCK
        ).quantize(Decimal("0.01"))

        self._db.add(
            Resultado(
                simulacao_id=sim.id,
                potencia_kwp=calculo.potencia_kwp,
                geracao_kwh=geracao_kwh,
                economia_mensal=calculo.economia_mensal,
                payback_anos=Decimal(payback_anos_int),
                payback_meses=Decimal(payback_meses_int),
                custo_total=calculo.investimento,
            )
        )
        sim.status = StatusSimulacao.CONCLUIDA

    def _carregar_simulacao(self, simulacao_id: uuid.UUID) -> Simulacao | None:
        stmt = (
            select(Simulacao)
            .where(Simulacao.id == simulacao_id)
            .options(
                selectinload(Simulacao.dados_consumo),
                selectinload(Simulacao.localizacao),
                selectinload(Simulacao.dados_telhado),
                selectinload(Simulacao.resultado).selectinload(Resultado.projecoes),
            )
        )
        return self._db.scalars(stmt).first()

    async def executar(
        self, usuario_id: uuid.UUID, simulacao_id: uuid.UUID
    ) -> SimulacaoExecutada:
        sim = self.obter(usuario_id, simulacao_id)

        if sim.status == StatusSimulacao.CONCLUIDA and sim.resultado:
            return SimulacaoExecutada(
                simulacao=sim,
                payback_texto=formatar_payback(
                    int(sim.resultado.payback_anos or 0),
                    int(sim.resultado.payback_meses or 0),
                ),
            )

        consumo = sim.dados_consumo
        loc = sim.localizacao
        telhado = sim.dados_telhado

        if not consumo or not loc or not telhado:
            raise DomainError("Simulação incompleta. Crie um rascunho válido primeiro.")

        if not loc.cep:
            raise DomainError("CEP obrigatório para executar a simulação (RB02).")

        sim.status = StatusSimulacao.VALIDANDO_DADOS
        self._db.commit()

        estado_uf = (loc.estado or "").upper() or None
        try:
            latitude, longitude, estado_uf, cidade_api = await buscar_cep_brasil_api(
                loc.cep
            )
            loc.latitude = latitude
            loc.longitude = longitude
            loc.estado = estado_uf
            loc.cidade = cidade_api or loc.cidade
        except (httpx.HTTPError, KeyError, InvalidOperation, TypeError, ValueError) as exc:
            logger.warning("Brasil API indisponível, usando fallback geográfico: %s", exc)

        tarifa_kwh = tarifa_por_uf(estado_uf)
        loc.tarifa_kwh = tarifa_kwh

        sim.status = StatusSimulacao.BUSCANDO_IRRADIACAO
        self._db.commit()

        hsp = HSP_FALLBACK
        if loc.latitude is not None and loc.longitude is not None:
            try:
                hsp = await buscar_hsp_nasa_power(loc.latitude, loc.longitude)
            except (httpx.HTTPError, KeyError, InvalidOperation, TypeError, ValueError) as exc:
                logger.warning("NASA POWER indisponível, usando HSP fallback: %s", exc)
        loc.hsp = hsp

        consumo_mensal_kwh = self._resolver_consumo_kwh(consumo, tarifa_kwh)

        sim.status = StatusSimulacao.CALCULANDO
        self._db.commit()

        entrada = EntradaCalculo(
            consumo_mensal_kwh=consumo_mensal_kwh,
            tarifa_kwh=tarifa_kwh,
            hsp=hsp,
            area_disponivel_m2=telhado.area_m2,
            tipo_conexao=telhado.tipo_conexao.value,
        )
        dimensionamento = calcular_dimensionamento(entrada)
        projecoes = projetar_25_anos(
            entrada,
            dimensionamento.investimento_total,
            dimensionamento.economia_mensal,
        )

        marcas_texto = MARCAS_FALLBACK
        observacao_gemini: str | None = None
        try:
            marcas_texto = await recomendar_equipamentos_gemini(
                dimensionamento.potencia_kwp,
                estado_uf or "BR",
            )
            observacao_gemini = marcas_texto
        except Exception as exc:
            logger.warning("Gemini API indisponível, usando marcas fallback: %s", exc)

        if sim.resultado:
            for proj in list(sim.resultado.projecoes):
                self._db.delete(proj)
            self._db.delete(sim.resultado)
            self._db.flush()

        resultado = Resultado(
            simulacao_id=sim.id,
            potencia_kwp=dimensionamento.potencia_kwp,
            quantidade_paineis=dimensionamento.quantidade_paineis,
            area_minima_m2=dimensionamento.area_minima_m2,
            geracao_kwh=dimensionamento.geracao_mensal_kwh,
            economia_mensal=dimensionamento.economia_mensal,
            payback_anos=Decimal(dimensionamento.payback_anos),
            payback_meses=Decimal(dimensionamento.payback_meses),
            custo_total=dimensionamento.investimento_total,
            marcas_recomendadas=marcas_texto,
            observacao_gemini=observacao_gemini,
        )
        self._db.add(resultado)
        self._db.flush()

        for ponto in projecoes:
            self._db.add(
                ProjecaoAnual(
                    resultado_id=resultado.id,
                    ano=ponto.ano,
                    custo_concessionaria=ponto.custo_concessionaria,
                    custo_fotovoltaico=ponto.custo_fotovoltaico,
                    saldo=ponto.saldo,
                )
            )

        if consumo.tipo_entrada == TipoEntradaConsumo.REAIS and consumo.valor_reais:
            consumo.consumo_kwh = consumo_mensal_kwh

        sim.status = StatusSimulacao.CONCLUIDA
        self._db.commit()
        self._db.refresh(sim)

        payback_texto = formatar_payback(
            dimensionamento.payback_anos,
            dimensionamento.payback_meses,
        )
        return SimulacaoExecutada(simulacao=sim, payback_texto=payback_texto)

    def _resolver_consumo_kwh(
        self, consumo: DadosConsumo, tarifa_kwh: Decimal
    ) -> Decimal:
        if consumo.consumo_kwh and consumo.consumo_kwh > 0:
            return consumo.consumo_kwh
        if consumo.valor_reais and consumo.valor_reais > 0:
            return (consumo.valor_reais / tarifa_kwh).quantize(Decimal("0.01"))
        raise DomainError("Informe consumo em kWh ou valor em reais (RB01).")
