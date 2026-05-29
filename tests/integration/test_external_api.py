"""Integração HTTP real (httpx) com APIs externas mockadas via respx."""

from __future__ import annotations

import httpx
import pytest
import respx

from app.domain.exceptions import ExternalApiError
from app.infrastructure.external.brasil_api import BrasilApiClient
from app.infrastructure.external.nasa_power import NasaPowerClient


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


class TestBrasilApiIntegration:
    async def test_buscar_cep_fluxo_completo_httpx(self) -> None:
        cep_payload = {
            "cep": "01310100",
            "state": "SP",
            "city": "São Paulo",
            "location": {"coordinates": {"latitude": -23.55, "longitude": -46.63}},
        }
        with respx.mock:
            respx.get("https://brasilapi.com.br/api/cep/v2/01310100").respond(
                200, json=cep_payload
            )
            result = await BrasilApiClient().buscar_cep("01310-100")

        assert result["city"] == "São Paulo"

    async def test_timeout_propaga_external_api_error(self) -> None:
        with respx.mock:
            respx.get(url__regex=r".*brasilapi.*").mock(
                side_effect=httpx.TimeoutException("timeout")
            )
            with pytest.raises(ExternalApiError) as exc_info:
                await BrasilApiClient().buscar_cep("01310100")

        assert exc_info.value.api_name == "Brasil API"


class TestNasaPowerIntegration:
    async def test_buscar_irradiacao_parse_json(self) -> None:
        nasa_json = {
            "properties": {
                "parameter": {"ALLSKY_SFC_SW_DWN": {"202001": 5.2}}
            }
        }
        with respx.mock:
            respx.get(url__regex=r".*power\.larc\.nasa\.gov.*").respond(
                200, json=nasa_json
            )
            result = await NasaPowerClient().buscar_irradiacao_mensal(-23.55, -46.63)

        assert "properties" in result

    async def test_http_500_mapeia_para_external_api_error(self) -> None:
        with respx.mock:
            respx.get(url__regex=r".*power\.larc\.nasa\.gov.*").respond(500)
            with pytest.raises(ExternalApiError) as exc_info:
                await NasaPowerClient().buscar_irradiacao_mensal(0.0, 0.0)

        assert exc_info.value.api_name == "NASA POWER"
