"""Marcadores de escopo futuro — hardware, exportação e motor de cálculo."""

from __future__ import annotations

import pytest


pytestmark = pytest.mark.integration


@pytest.mark.skip(reason="Módulo pyvisa/SCPI ainda não existe no SolarCalc")
def test_scpi_visa_quando_implementado() -> None:
    """Placeholder: integrar FakeVisaInstrument com camada de instrumentos."""
    ...


@pytest.mark.skip(reason="Comunicação serial ainda não existe no SolarCalc")
def test_serial_quando_implementado() -> None:
    """Placeholder: integrar FakeSerial com drivers de bancada."""
    ...


@pytest.mark.skip(reason="Exportação CSV/XLSX/S2P ainda não implementada")
def test_exportacao_resultados() -> None:
    """Placeholder: validar round-trip de arquivos gerados pelo motor."""
    ...
