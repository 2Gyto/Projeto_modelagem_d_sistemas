"""Testes do motor simplificado com mocks (Micro-etapa A)."""

from decimal import Decimal

import pytest

from app.application.simulacao_service import (
    CUSTO_POR_KWP_MOCK,
    DIAS_MES_MOCK,
    EFICIENCIA_MOCK,
    HSP_MOCK,
    KWH_TAXA_MINIMA_MOCK,
    TARIFA_MOCK,
    calcular_com_mocks,
)
from app.domain.exceptions import DomainError


def test_consumo_a_partir_de_valor_reais() -> None:
    valor = Decimal("300")
    resultado = calcular_com_mocks(valor_reais=valor, consumo_kwh=None)

    consumo_esperado = (valor / TARIFA_MOCK).quantize(Decimal("0.01"))
    assert resultado.consumo_kwh == consumo_esperado

    potencia_esperada = (
        (consumo_esperado / DIAS_MES_MOCK) / (HSP_MOCK * EFICIENCIA_MOCK)
    ).quantize(Decimal("0.01"))
    assert resultado.potencia_kwp == potencia_esperada
    assert resultado.investimento == (potencia_esperada * CUSTO_POR_KWP_MOCK).quantize(
        Decimal("0.01")
    )

    economia_esperada = (
        valor - (KWH_TAXA_MINIMA_MOCK * TARIFA_MOCK)
    ).quantize(Decimal("0.01"))
    assert resultado.economia_mensal == economia_esperada

    payback_esperado = (
        resultado.investimento / (economia_esperada * Decimal("12"))
    ).quantize(Decimal("0.01"))
    assert resultado.payback_anos == payback_esperado


def test_consumo_kwh_direto() -> None:
    consumo = Decimal("350")
    resultado = calcular_com_mocks(valor_reais=None, consumo_kwh=consumo)

    assert resultado.consumo_kwh == consumo
    gasto = (consumo * TARIFA_MOCK).quantize(Decimal("0.01"))
    economia_esperada = (
        gasto - (KWH_TAXA_MINIMA_MOCK * TARIFA_MOCK)
    ).quantize(Decimal("0.01"))
    assert resultado.economia_mensal == economia_esperada


def test_rb01_sem_entrada() -> None:
    with pytest.raises(DomainError, match="RB01"):
        calcular_com_mocks(valor_reais=None, consumo_kwh=None)
