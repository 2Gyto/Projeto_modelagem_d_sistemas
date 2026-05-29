"""Testes auxiliares da persistência (Micro-etapa B)."""

from decimal import Decimal

from app.application.simulacao_service import _decompor_payback


def test_decompor_payback_decimal() -> None:
    anos, meses = _decompor_payback(Decimal("4.37"))
    assert anos == 4
    assert meses == 4
