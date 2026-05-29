"""Cálculo simplificado de dimensionamento fotovoltaico (MVP).

Premissas (parâmetros médios brasileiros, ajustáveis):
- Tarifa média: R$ 0,85/kWh
- HSP (Horas de Sol Pleno) médio: 5 h/dia
- Potência por painel: 550 W (0,55 kWp)
- Eficiência efetiva do sistema (perdas + inversor): 80%
- 30 dias/mês
"""

from dataclasses import dataclass
from decimal import Decimal
from math import ceil

TARIFA_PADRAO_REAIS_KWH = Decimal("0.85")
HSP_PADRAO_HORAS_DIA = Decimal("5.0")
POTENCIA_PAINEL_KWP = Decimal("0.55")
EFICIENCIA_SISTEMA = Decimal("0.80")
DIAS_MES = Decimal("30")


@dataclass(frozen=True)
class ResultadoCalculo:
    consumo_kwh_mes: Decimal
    geracao_por_painel_kwh_mes: Decimal
    quantidade_paineis: int
    geracao_total_kwh_mes: Decimal
    potencia_sistema_kwp: Decimal
    economia_mensal_reais: Decimal


def calcular_paineis_por_gasto(
    valor_reais_mes: Decimal,
    tarifa_kwh: Decimal = TARIFA_PADRAO_REAIS_KWH,
    hsp: Decimal = HSP_PADRAO_HORAS_DIA,
) -> ResultadoCalculo:
    consumo_kwh = (valor_reais_mes / tarifa_kwh).quantize(Decimal("0.01"))

    geracao_painel = (
        POTENCIA_PAINEL_KWP * hsp * DIAS_MES * EFICIENCIA_SISTEMA
    ).quantize(Decimal("0.01"))

    quantidade = max(1, ceil(consumo_kwh / geracao_painel))

    geracao_total = (geracao_painel * quantidade).quantize(Decimal("0.01"))
    potencia_sistema = (POTENCIA_PAINEL_KWP * quantidade).quantize(Decimal("0.01"))
    economia = min(consumo_kwh, geracao_total) * tarifa_kwh

    return ResultadoCalculo(
        consumo_kwh_mes=consumo_kwh,
        geracao_por_painel_kwh_mes=geracao_painel,
        quantidade_paineis=quantidade,
        geracao_total_kwh_mes=geracao_total,
        potencia_sistema_kwp=potencia_sistema,
        economia_mensal_reais=economia.quantize(Decimal("0.01")),
    )
