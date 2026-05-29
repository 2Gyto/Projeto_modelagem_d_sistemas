"""Motor de cálculo fotovoltaico e financeiro (RF05–RF07, RB01–RB10)."""

from decimal import Decimal, ROUND_HALF_UP

from app.domain.calculo import (
    ANOS_PROJECAO,
    AREA_PAINEL_M2,
    CUSTO_POR_KWP_BRL,
    DIAS_NO_MES,
    EFICIENCIA_SISTEMA,
    INFLACAO_ENERGIA_ANUAL,
    MANUTENCAO_ANUAL_PCT,
    POTENCIA_PAINEL_WP,
    TAXA_DISPONIBILIDADE_KWH,
    EntradaCalculo,
    PontoProjecao,
    ResultadoDimensionamento,
)
from app.domain.exceptions import DomainError


def _q2(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _consumo_diario(consumo_mensal_kwh: Decimal) -> Decimal:
    return consumo_mensal_kwh / DIAS_NO_MES


def _potencia_kwp_necessaria(consumo_diario: Decimal, hsp: Decimal) -> Decimal:
    """Potência (kWp) = consumo diário / (HSP × eficiência do sistema)."""
    if hsp <= 0:
        raise DomainError("Índice HSP inválido para dimensionamento (RB03).")
    divisor = hsp * EFICIENCIA_SISTEMA
    return _q2(consumo_diario / divisor)


def _geracao_mensal_kwh(potencia_kwp: Decimal, hsp: Decimal) -> Decimal:
    """Geração mensal (kWh) = kWp × HSP × dias × eficiência."""
    return _q2(potencia_kwp * hsp * DIAS_NO_MES * EFICIENCIA_SISTEMA)


def _quantidade_paineis(potencia_kwp: Decimal) -> int:
    from math import ceil

    potencia_wp = potencia_kwp * Decimal("1000")
    return int(ceil(float(potencia_wp / POTENCIA_PAINEL_WP)))


def _area_minima_m2(quantidade_paineis: int) -> Decimal:
    return _q2(Decimal(quantidade_paineis) * AREA_PAINEL_M2)


def _ajustar_por_area(
    potencia_kwp: Decimal,
    area_disponivel_m2: Decimal,
) -> tuple[Decimal, int, Decimal]:
    """RB04 — limita painéis à área informada."""
    qtd = _quantidade_paineis(potencia_kwp)
    area_necessaria = _area_minima_m2(qtd)
    if area_necessaria <= area_disponivel_m2:
        return potencia_kwp, qtd, area_necessaria

    max_paineis = int(area_disponivel_m2 / AREA_PAINEL_M2)
    if max_paineis < 1:
        raise DomainError(
            "Área disponível insuficiente para instalar ao menos um painel (RB04)."
        )
    potencia_ajustada = _q2(
        (Decimal(max_paineis) * POTENCIA_PAINEL_WP) / Decimal("1000")
    )
    return potencia_ajustada, max_paineis, _area_minima_m2(max_paineis)


def _custo_minimo_faturado(tarifa_kwh: Decimal, tipo_conexao: str) -> Decimal:
    kwh_min = TAXA_DISPONIBILIDADE_KWH.get(tipo_conexao.upper(), Decimal("30"))
    return _q2(kwh_min * tarifa_kwh)


def _economia_mensal(
    consumo_mensal_kwh: Decimal,
    geracao_mensal_kwh: Decimal,
    tarifa_kwh: Decimal,
    custo_minimo: Decimal,
) -> Decimal:
    energia_compensada = min(consumo_mensal_kwh, geracao_mensal_kwh)
    economia_bruta = _q2(energia_compensada * tarifa_kwh)
    economia = _q2(economia_bruta - custo_minimo)
    if economia <= 0:
        raise DomainError(
            "Economia mensal insuficiente para viabilizar o investimento."
        )
    return economia


def _payback(investimento: Decimal, economia_mensal: Decimal) -> tuple[int, int]:
    meses_totais = int(
        (investimento / economia_mensal).to_integral_value(rounding=ROUND_HALF_UP)
    )
    anos = meses_totais // 12
    meses = meses_totais % 12
    return anos, meses


def calcular_dimensionamento(entrada: EntradaCalculo) -> ResultadoDimensionamento:
    """Executa dimensionamento físico-financeiro completo."""
    if entrada.consumo_mensal_kwh <= 0 or entrada.tarifa_kwh <= 0:
        raise DomainError("Consumo e tarifa devem ser maiores que zero (RB01).")

    consumo_diario = _consumo_diario(entrada.consumo_mensal_kwh)
    potencia_kwp = _potencia_kwp_necessaria(consumo_diario, entrada.hsp)
    potencia_kwp, qtd_paineis, area_min = _ajustar_por_area(
        potencia_kwp, entrada.area_disponivel_m2
    )

    geracao = _geracao_mensal_kwh(potencia_kwp, entrada.hsp)
    investimento = _q2(potencia_kwp * CUSTO_POR_KWP_BRL)
    custo_minimo = _custo_minimo_faturado(entrada.tarifa_kwh, entrada.tipo_conexao)
    economia = _economia_mensal(
        entrada.consumo_mensal_kwh,
        geracao,
        entrada.tarifa_kwh,
        custo_minimo,
    )
    anos, meses = _payback(investimento, economia)

    return ResultadoDimensionamento(
        potencia_kwp=potencia_kwp,
        quantidade_paineis=qtd_paineis,
        area_minima_m2=area_min,
        geracao_mensal_kwh=geracao,
        investimento_total=investimento,
        economia_mensal=economia,
        payback_anos=anos,
        payback_meses=meses,
    )


def projetar_25_anos(
    entrada: EntradaCalculo,
    investimento: Decimal,
    economia_mensal: Decimal,
) -> list[PontoProjecao]:
    """Projeção acumulada para dashboard comparativo (RF07 / RB06)."""
    custo_anual_inicial = _q2(entrada.consumo_mensal_kwh * entrada.tarifa_kwh * Decimal("12"))
    custo_acum_concessionaria = Decimal("0")
    custo_acum_fotovoltaico = investimento
    economia_anual = _q2(economia_mensal * Decimal("12"))
    pontos: list[PontoProjecao] = []

    for ano in range(ANOS_PROJECAO + 1):
        if ano == 0:
            pontos.append(
                PontoProjecao(
                    ano=0,
                    custo_concessionaria=Decimal("0"),
                    custo_fotovoltaico=investimento,
                    saldo=_q2(investimento * -1),
                )
            )
            continue

        fator = (Decimal("1") + INFLACAO_ENERGIA_ANUAL) ** ano
        custo_ano = _q2(custo_anual_inicial * fator)
        custo_acum_concessionaria = _q2(custo_acum_concessionaria + custo_ano)
        manutencao = _q2(investimento * MANUTENCAO_ANUAL_PCT)
        custo_acum_fotovoltaico = _q2(
            investimento + manutencao * Decimal(ano) - economia_anual * Decimal(ano)
        )
        saldo = _q2(custo_acum_concessionaria - custo_acum_fotovoltaico)
        pontos.append(
            PontoProjecao(
                ano=ano,
                custo_concessionaria=custo_acum_concessionaria,
                custo_fotovoltaico=custo_acum_fotovoltaico,
                saldo=saldo,
            )
        )
    return pontos


def formatar_payback(anos: int, meses: int) -> str:
    if anos == 0:
        return f"{meses} meses"
    if meses == 0:
        return f"{anos} anos"
    return f"{anos} anos e {meses} meses"
