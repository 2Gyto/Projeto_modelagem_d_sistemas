"""Testes dos clientes Brasil API e NASA POWER com HTTP mockado."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.domain.exceptions import ExternalApiError
from app.infrastructure.external.brasil_api import BrasilApiClient
from app.infrastructure.external.nasa_power import NasaPowerClient


def _patch_client_get(return_value: dict) -> MagicMock:
    """Stub de response.json() para métodos de alto nível."""
    response = MagicMock(spec=httpx.Response)
    response.json.return_value = return_value
    response.raise_for_status = MagicMock()
    return response


@pytest.mark.asyncio
class TestBrasilApiClient:
    async def test_buscar_cep_remove_caracteres_nao_numericos(self) -> None:
        # Objetivo: CEP formatado (01310-100) vira apenas dígitos na URL.
        payload = {"cep": "01310100", "city": "São Paulo"}
        response = _patch_client_get(payload)

        with patch.object(
            BrasilApiClient,
            "get",
            new_callable=AsyncMock,
            return_value=response,
        ) as mock_get:
            client = BrasilApiClient()
            result = await client.buscar_cep("01310-100")

        assert result == payload
        mock_get.assert_awaited_once()
        path = mock_get.await_args.args[0]
        assert path == "/cep/v2/01310100"

    async def test_buscar_cep_propaga_external_api_error(self) -> None:
        # Objetivo: falha na Brasil API sobe como ExternalApiError.
        with patch.object(
            BrasilApiClient,
            "get",
            new_callable=AsyncMock,
            side_effect=ExternalApiError("Brasil API", "falha"),
        ):
            with pytest.raises(ExternalApiError):
                await BrasilApiClient().buscar_cep("00000000")


@pytest.mark.asyncio
class TestNasaPowerClient:
    async def test_buscar_irradiacao_monta_path_com_coordenadas(self) -> None:
        # Objetivo: consulta NASA inclui latitude/longitude e parâmetro de irradiação.
        payload = {"properties": {"parameter": {}}}
        response = _patch_client_get(payload)

        with patch.object(
            NasaPowerClient,
            "get",
            new_callable=AsyncMock,
            return_value=response,
        ) as mock_get:
            client = NasaPowerClient()
            result = await client.buscar_irradiacao_mensal(-23.55, -46.63)

        assert result == payload
        path = mock_get.await_args.args[0]
        assert "latitude=-23.55" in path
        assert "longitude=-46.63" in path
        assert "ALLSKY_SFC_SW_DWN" in path
