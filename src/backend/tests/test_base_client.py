"""Testes do cliente HTTP base — timeouts e erros viram ExternalApiError."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.domain.exceptions import ExternalApiError
from app.infrastructure.external.base_client import BaseHttpClient


class _TestClient(BaseHttpClient):
    """Subclasse mínima para exercitar get() sem depender de APIs reais."""


def _mock_async_client(response: httpx.Response | None = None, **get_kwargs) -> AsyncMock:
    """Monta mock do context manager httpx.AsyncClient."""
    mock_client = AsyncMock()
    if response is not None:
        mock_client.get = AsyncMock(return_value=response)
    else:
        mock_client.get = AsyncMock(**get_kwargs)
    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_client)
    mock_cm.__aexit__ = AsyncMock(return_value=None)
    return mock_cm


@pytest.mark.asyncio
class TestBaseHttpClient:
    async def test_get_retorna_response_em_sucesso(self) -> None:
        # Objetivo: chamadas HTTP bem-sucedidas propagam o response.
        response = MagicMock(spec=httpx.Response)
        response.raise_for_status = MagicMock()

        with patch(
            "app.infrastructure.external.base_client.httpx.AsyncClient",
            return_value=_mock_async_client(response=response),
        ):
            client = _TestClient("API Teste", "https://api.example.com")
            result = await client.get("/recurso")

        assert result is response
        response.raise_for_status.assert_called_once()

    async def test_get_lanca_external_api_error_em_timeout(self) -> None:
        # Objetivo: timeout não derruba a app — vira 503 com mensagem amigável (ADR-03).
        mock_cm = _mock_async_client()
        inner = await mock_cm.__aenter__()
        inner.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))

        with patch(
            "app.infrastructure.external.base_client.httpx.AsyncClient",
            return_value=mock_cm,
        ):
            client = _TestClient("API Teste", "https://api.example.com")
            with pytest.raises(ExternalApiError) as exc_info:
                await client.get("/lento")

        assert exc_info.value.api_name == "API Teste"
        assert "indisponível" in str(exc_info.value).lower()

    async def test_get_lanca_external_api_error_em_http_error(self) -> None:
        # Objetivo: 4xx/5xx após raise_for_status viram ExternalApiError.
        response = MagicMock(spec=httpx.Response)
        response.raise_for_status = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "erro",
                request=MagicMock(),
                response=response,
            )
        )
        mock_cm = _mock_async_client(response=response)

        with patch(
            "app.infrastructure.external.base_client.httpx.AsyncClient",
            return_value=mock_cm,
        ):
            client = _TestClient("API Teste", "https://api.example.com")
            with pytest.raises(ExternalApiError, match="comunicação"):
                await client.get("/falha")

    async def test_base_url_remove_barra_final(self) -> None:
        # Edge case: URLs com trailing slash não duplicam barras no path.
        client = _TestClient("X", "https://host.com/")
        assert client.base_url == "https://host.com"
