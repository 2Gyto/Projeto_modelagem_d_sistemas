"""Testes unitários do motor de cálculo (sem APIs externas)."""

from decimal import Decimal

import pytest

from app.application.calculo_simulacao import calcular_dimensionamento, projetar_25_anos
from app.domain.calculo import EntradaCalculo
from app.domain.exceptions import DomainError


def _entrada() -> EntradaCalculo:
    return EntradaCalculo(
        consumo_mensal_kwh=Decimal("350"),
        tarifa_kwh=Decimal("0.83"),
        hsp=Decimal("5.2"),
        area_disponivel_m2=Decimal("40"),
        tipo_conexao="MONOFASICA",
    )


def test_dimensionamento_basico() -> None:
    resultado = calcular_dimensionamento(_entrada())
    assert resultado.quantidade_paineis >= 1
    assert resultado.potencia_kwp > 0
    assert resultado.investimento_total == resultado.potencia_kwp * Decimal("3800")
    assert resultado.economia_mensal > 0
    assert resultado.payback_anos >= 0


def test_rb04_area_insuficiente() -> None:
    entrada = EntradaCalculo(
        consumo_mensal_kwh=Decimal("800"),
        tarifa_kwh=Decimal("0.83"),
        hsp=Decimal("5.2"),
        area_disponivel_m2=Decimal("2"),
        tipo_conexao="MONOFASICA",
    )
    with pytest.raises(DomainError, match="Área disponível insuficiente"):
        calcular_dimensionamento(entrada)


def test_projecao_25_anos() -> None:
    entrada = _entrada()
    dim = calcular_dimensionamento(entrada)
    pontos = projetar_25_anos(entrada, dim.investimento_total, dim.economia_mensal)
    assert len(pontos) == 26
    assert pontos[0].ano == 0
    assert pontos[0].custo_fotovoltaico == dim.investimento_total
