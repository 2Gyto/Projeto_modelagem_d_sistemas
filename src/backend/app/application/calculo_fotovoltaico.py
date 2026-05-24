"""Motor de cálculo RF05–RF07 e regras RB04–RB06."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from app.config import Settings
from app.domain.enums import OrientacaoTelhado, TipoConexao
from app.infrastructure.db.tarifa_sqlite import TarifaUf

_TWO = Decimal("0.01")


@dataclass(frozen=True)
class EntradaCalculo:
    consumo_kwh_mes: Decimal
    area_m2: Decimal
    orientacao: OrientacaoTelhado
    tipo_conexao: TipoConexao
    hsp_medio_dia: Decimal
    tarifa: TarifaUf


@dataclass(frozen=True)
class ProjecaoAno:
    ano: int
    custo_concessionaria: Decimal
    custo_fotovoltaico: Decimal


@dataclass(frozen=True)
class ResultadoCalculo:
    consumo_kwh_mes: Decimal
    consumo_faturado_kwh: Decimal
    tarifa_kwh: Decimal
    hsp_medio_dia: Decimal
    qtd_paineis: int
    potencia_kwp: Decimal
    geracao_kwh_mes: Decimal
    investimento: Decimal
    economia_mensal: Decimal
    payback_anos: int
    payback_meses: int
    lucro_25_anos: Decimal
    ano_payback: int
    projecoes: list[ProjecaoAno]
    marcas: str


_FATOR_ORIENTACAO = {
    OrientacaoTelhado.NORTE: Decimal("1.00"),
    OrientacaoTelhado.LESTE: Decimal("0.85"),
    OrientacaoTelhado.OESTE: Decimal("0.85"),
    OrientacaoTelhado.SUL: Decimal("0.70"),
}


def _money(value: Decimal) -> Decimal:
    return value.quantize(_TWO, rounding=ROUND_HALF_UP)


def _taxa_disponibilidade_kwh(tarifa: TarifaUf, tipo: TipoConexao) -> Decimal:
    if tipo == TipoConexao.MONOFASICA:
        return tarifa.taxa_disponibilidade_mono
    if tipo == TipoConexao.BIFASICA:
        return tarifa.taxa_disponibilidade_bi
    return tarifa.taxa_disponibilidade_tri


class CalculoFotovoltaicoService:
    def __init__(self, settings: Settings) -> None:
        self._s = settings

    def calcular(self, entrada: EntradaCalculo) -> ResultadoCalculo:
        tarifa_kwh = entrada.tarifa.tarifa_kwh
        taxa_min = _taxa_disponibilidade_kwh(entrada.tarifa, entrada.tipo_conexao)
        consumo_faturado = max(entrada.consumo_kwh_mes, taxa_min)

        area_painel = Decimal(str(self._s.area_por_painel_m2))
        potencia_painel = Decimal(str(self._s.potencia_painel_kw))
        preco_painel = Decimal(str(self._s.preco_painel_brl))
        eficiencia = Decimal(str(self._s.eficiencia_sistema))

        qtd_paineis = int(entrada.area_m2 / area_painel)
        if qtd_paineis < 1:
            raise ValueError("Área insuficiente para instalar painéis. (RB04)")

        potencia_kwp = _money(potencia_painel * qtd_paineis)
        fator_orient = _FATOR_ORIENTACAO[entrada.orientacao]
        geracao_kwh_mes = _money(
            potencia_kwp
            * entrada.hsp_medio_dia
            * Decimal("30")
            * eficiencia
            * fator_orient
        )

        energia_compensada = min(geracao_kwh_mes, consumo_faturado)
        economia_mensal = _money(energia_compensada * tarifa_kwh)
        investimento = _money(preco_painel * qtd_paineis)

        if economia_mensal <= 0:
            payback_anos, payback_meses, ano_payback = 99, 0, 99
        else:
            meses_total = int(
                (investimento / economia_mensal).to_integral_value(rounding=ROUND_HALF_UP)
            )
            if meses_total < 1:
                meses_total = 1
            payback_anos = meses_total // 12
            payback_meses = meses_total % 12
            ano_payback = payback_anos if payback_meses == 0 else payback_anos + 1

        inflacao = Decimal(str(self._s.inflacao_energia_anual))
        manutencao_pct = Decimal(str(self._s.manutencao_anual_pct))
        anos = self._s.anos_projecao

        projecoes: list[ProjecaoAno] = []
        acum_conc = Decimal("0")
        acum_solar = investimento

        projecoes.append(
            ProjecaoAno(
                ano=0,
                custo_concessionaria=Decimal("0"),
                custo_fotovoltaico=_money(acum_solar),
            )
        )

        custo_anual_base = _money(consumo_faturado * tarifa_kwh * Decimal("12"))

        for ano in range(1, anos + 1):
            fator = (Decimal("1") + inflacao) ** (ano - 1)
            custo_ano_conc = _money(custo_anual_base * fator)
            acum_conc += custo_ano_conc
            manutencao = _money(investimento * manutencao_pct)
            acum_solar += manutencao
            projecoes.append(
                ProjecaoAno(
                    ano=ano,
                    custo_concessionaria=_money(acum_conc),
                    custo_fotovoltaico=_money(acum_solar),
                )
            )

        custo_total_conc = projecoes[-1].custo_concessionaria
        custo_total_solar = projecoes[-1].custo_fotovoltaico
        lucro_25_anos = _money(custo_total_conc - custo_total_solar)

        return ResultadoCalculo(
            consumo_kwh_mes=_money(entrada.consumo_kwh_mes),
            consumo_faturado_kwh=_money(consumo_faturado),
            tarifa_kwh=tarifa_kwh,
            hsp_medio_dia=_money(entrada.hsp_medio_dia),
            qtd_paineis=qtd_paineis,
            potencia_kwp=potencia_kwp,
            geracao_kwh_mes=geracao_kwh_mes,
            investimento=investimento,
            economia_mensal=economia_mensal,
            payback_anos=payback_anos,
            payback_meses=payback_meses,
            lucro_25_anos=lucro_25_anos,
            ano_payback=ano_payback,
            projecoes=projecoes,
            marcas=self._s.marcas_paineis,
        )
