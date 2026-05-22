import logging

import httpx

from app.config import get_settings
from app.domain.exceptions import ExternalApiError

logger = logging.getLogger(__name__)
_settings = get_settings()


class BaseHttpClient:
    def __init__(self, api_name: str, base_url: str) -> None:
        self.api_name = api_name
        self.base_url = base_url.rstrip("/")
        self.timeout = _settings.external_api_timeout_seconds

    async def get(self, path: str, **kwargs) -> httpx.Response:
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, **kwargs)
                response.raise_for_status()
                return response
        except httpx.TimeoutException as exc:
            logger.warning("%s timeout: %s", self.api_name, url)
            raise ExternalApiError(
                self.api_name,
                "Serviço temporariamente indisponível. Tente novamente mais tarde.",
            ) from exc
        except httpx.HTTPError as exc:
            logger.exception("%s falhou: %s", self.api_name, url)
            raise ExternalApiError(
                self.api_name,
                "Falha na comunicação com serviço externo.",
            ) from exc
