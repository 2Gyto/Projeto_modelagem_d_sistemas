import json
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.domain.enums import StatusSimulacao


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)


class UsuarioResponse(BaseModel):
    id: uuid.UUID
    nome: str
    email: str
    criado_em: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SimulacaoCreate(BaseModel):
    """Entrada mínima para iniciar uma simulação (RF01–RF04)."""

    consumo_kwh: Decimal | None = Field(default=None, gt=0)
    valor_reais: Decimal | None = Field(default=None, gt=0)
    tipo_entrada: str
    cep: str | None = Field(default=None, min_length=8, max_length=9)
    cidade: str | None = None
    area_m2: Decimal = Field(gt=0)
    orientacao: str
    tipo_conexao: str
    concessionaria: str | None = None


class RecomendacoesGeminiResponse(BaseModel):
    tarifa_kwh: Decimal
    marcas_paineis: list[str]
    observacao: str | None = None


class DadosTecnicosResponse(BaseModel):
    potencia_kwp: Decimal
    quantidade_paineis: int
    area_minima_m2: Decimal
    geracao_mensal_kwh: Decimal
    hsp: Decimal
    latitude: Decimal
    longitude: Decimal
    estado: str
    cidade: str | None = None


class DadosFinanceirosResponse(BaseModel):
    investimento_total: Decimal
    economia_mensal: Decimal
    payback_anos: int
    payback_meses: int
    payback_texto: str
    tarifa_kwh: Decimal
    lucro_25_anos: Decimal | None = None


class GraficoComparativoResponse(BaseModel):
    anos: list[int]
    custo_acumulado_concessionaria: list[float]
    custo_acumulado_fotovoltaico: list[float]
    saldo_acumulado: list[float]


class SimulacaoResponse(BaseModel):
    id: uuid.UUID
    status: StatusSimulacao
    realizada_em: datetime

    model_config = {"from_attributes": True}


class SimulacaoResultadoResponse(BaseModel):
    """Resultado do motor com mocks (Micro-etapas A/B), persistido em `resultados`."""

    simulacao_id: uuid.UUID
    status: StatusSimulacao
    consumo_kwh: Decimal
    potencia_kwp: Decimal
    investimento: Decimal
    economia_mensal: Decimal
    payback_anos: Decimal
    tarifa_mock: Decimal = Decimal("0.83")
    hsp_mock: Decimal = Decimal("4.5")

    @classmethod
    def from_simulacao(cls, sim) -> "SimulacaoResultadoResponse":
        res = sim.resultado
        consumo = sim.dados_consumo
        if not res or not consumo:
            raise ValueError("Simulação sem resultado persistido.")

        payback_decimal = (res.payback_anos or Decimal("0")) + (
            (res.payback_meses or Decimal("0")) / Decimal("12")
        )

        return cls(
            simulacao_id=sim.id,
            status=sim.status,
            consumo_kwh=consumo.consumo_kwh or Decimal("0"),
            potencia_kwp=res.potencia_kwp or Decimal("0"),
            investimento=res.custo_total or Decimal("0"),
            economia_mensal=res.economia_mensal or Decimal("0"),
            payback_anos=payback_decimal.quantize(Decimal("0.01")),
            tarifa_mock=sim.localizacao.tarifa_kwh
            if sim.localizacao and sim.localizacao.tarifa_kwh
            else Decimal("0.83"),
            hsp_mock=sim.localizacao.hsp
            if sim.localizacao and sim.localizacao.hsp
            else Decimal("4.5"),
        )


class SimulacaoExecutarResponse(BaseModel):
    """Resposta completa após pipeline Brasil API → NASA → Gemini → cálculo."""

    id: uuid.UUID
    status: StatusSimulacao
    realizada_em: datetime
    resumo: DadosFinanceirosResponse
    tecnico: DadosTecnicosResponse
    recomendacoes: RecomendacoesGeminiResponse
    grafico: GraficoComparativoResponse

    @classmethod
    def from_simulacao(cls, sim, payback_texto: str) -> "SimulacaoExecutarResponse":
        loc = sim.localizacao
        res = sim.resultado
        if not loc or not res:
            raise ValueError("Simulação sem resultados persistidos.")

        marcas: list[str] = []
        if res.marcas_recomendadas:
            try:
                marcas = json.loads(res.marcas_recomendadas)
            except json.JSONDecodeError:
                marcas = [res.marcas_recomendadas]

        projecoes = sorted(res.projecoes, key=lambda p: p.ano)
        lucro_25 = None
        if projecoes:
            ultimo = projecoes[-1]
            lucro_25 = ultimo.saldo

        return cls(
            id=sim.id,
            status=sim.status,
            realizada_em=sim.realizada_em,
            resumo=DadosFinanceirosResponse(
                investimento_total=res.custo_total or Decimal("0"),
                economia_mensal=res.economia_mensal or Decimal("0"),
                payback_anos=int(res.payback_anos or 0),
                payback_meses=int(res.payback_meses or 0),
                payback_texto=payback_texto,
                tarifa_kwh=loc.tarifa_kwh or Decimal("0"),
                lucro_25_anos=lucro_25,
            ),
            tecnico=DadosTecnicosResponse(
                potencia_kwp=res.potencia_kwp or Decimal("0"),
                quantidade_paineis=res.quantidade_paineis or 0,
                area_minima_m2=res.area_minima_m2 or Decimal("0"),
                geracao_mensal_kwh=res.geracao_kwh or Decimal("0"),
                hsp=loc.hsp or Decimal("0"),
                latitude=loc.latitude or Decimal("0"),
                longitude=loc.longitude or Decimal("0"),
                estado=loc.estado or "",
                cidade=loc.cidade,
            ),
            recomendacoes=RecomendacoesGeminiResponse(
                tarifa_kwh=loc.tarifa_kwh or Decimal("0"),
                marcas_paineis=marcas,
                observacao=res.observacao_gemini,
            ),
            grafico=GraficoComparativoResponse(
                anos=[p.ano for p in projecoes],
                custo_acumulado_concessionaria=[
                    float(p.custo_concessionaria) for p in projecoes
                ],
                custo_acumulado_fotovoltaico=[
                    float(p.custo_fotovoltaico) for p in projecoes
                ],
                saldo_acumulado=[float(p.saldo) for p in projecoes],
            ),
        )


class HealthResponse(BaseModel):
    status: str
    app: str


class SimulacaoTesteRequest(BaseModel):
    nome: str
    cep: str
    gasto: str
    tipo: str
