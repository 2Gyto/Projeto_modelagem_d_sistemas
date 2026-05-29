"""Entidades de valor e constantes do motor de cálculo (RF05–RF07, RB01–RB10)."""

from dataclasses import dataclass
from decimal import Decimal

# Parâmetros de mercado (configuráveis — Visão do Produto / RF05)
POTENCIA_PAINEL_WP = Decimal("550")
AREA_PAINEL_M2 = Decimal("2.5")
CUSTO_POR_KWP_BRL = Decimal("3800")
EFICIENCIA_SISTEMA = Decimal("0.75")
DIAS_NO_MES = Decimal("30")
INFLACAO_ENERGIA_ANUAL = Decimal("0.05")
MANUTENCAO_ANUAL_PCT = Decimal("0.01")
ANOS_PROJECAO = 25

# Taxa mínima de disponibilidade (kWh) — RB05
TAXA_DISPONIBILIDADE_KWH: dict[str, Decimal] = {
    "MONOFASICA": Decimal("30"),
    "BIFASICA": Decimal("50"),
    "TRIFASICA": Decimal("100"),
}


@dataclass(frozen=True)
class EntradaCalculo:
    consumo_mensal_kwh: Decimal
    tarifa_kwh: Decimal
    hsp: Decimal
    area_disponivel_m2: Decimal
    tipo_conexao: str


@dataclass(frozen=True)
class ResultadoDimensionamento:
    potencia_kwp: Decimal
    quantidade_paineis: int
    area_minima_m2: Decimal
    geracao_mensal_kwh: Decimal
    investimento_total: Decimal
    economia_mensal: Decimal
    payback_anos: int
    payback_meses: int


@dataclass(frozen=True)
class PontoProjecao:
    ano: int
    custo_concessionaria: Decimal
    custo_fotovoltaico: Decimal
    saldo: Decimal
