import logging

import httpx

from app.config import get_settings
from app.domain.exceptions import DomainError, ExternalApiError
from app.domain.geo import EnderecoGeo
from app.infrastructure.external.base_client import BaseHttpClient

logger = logging.getLogger(__name__)
_settings = get_settings()


class BrasilApiClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("Brasil API", _settings.brasil_api_base_url)

    @staticmethod
    def _normalizar_cep(cep: str) -> str:
        cep_limpo = "".join(c for c in cep if c.isdigit())
        if len(cep_limpo) != 8:
            raise DomainError("CEP inválido. Informe 8 dígitos.")
        return cep_limpo

    async def buscar_cep(self, cep: str) -> dict:
        cep_limpo = self._normalizar_cep(cep)
        url = f"{self.base_url}/cep/v2/{cep_limpo}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                if response.status_code == 404:
                    raise DomainError("CEP não encontrado.")
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException as exc:
            logger.warning("Brasil API timeout: %s", url)
            raise ExternalApiError(
                "Brasil API",
                "Serviço temporariamente indisponível. Tente novamente mais tarde.",
            ) from exc
        except DomainError:
            raise
        except httpx.HTTPError as exc:
            logger.exception("Brasil API falhou: %s", url)
            raise ExternalApiError(
                "Brasil API",
                "Falha na comunicação com serviço externo.",
            ) from exc

    async def resolver_cep(self, cep: str) -> EnderecoGeo:
        """CEP V2 → UF, cidade, latitude e longitude."""
        data = await self.buscar_cep(cep)
        cep_limpo = self._normalizar_cep(cep)

        uf = data.get("state")
        cidade = data.get("city")
        if not uf or not cidade:
            raise DomainError("CEP sem dados de localização completos.")

        location = data.get("location") or {}
        coordinates = location.get("coordinates")
        latitude, longitude = _extrair_coordenadas(coordinates)
        if latitude is None or longitude is None:
            raise DomainError(
                "CEP sem coordenadas geográficas. Não é possível calcular o HSP."
            )

        return EnderecoGeo(
            cep=cep_limpo,
            uf=str(uf).upper(),
            cidade=str(cidade),
            latitude=latitude,
            longitude=longitude,
        )


def _extrair_coordenadas(coordinates: object) -> tuple[float | None, float | None]:
    """Suporta formato Brasil API v2 (dict) e GeoJSON (lista [lng, lat])."""
    if isinstance(coordinates, dict):
        lat = coordinates.get("latitude")
        lng = coordinates.get("longitude")
        if lat is not None and lng is not None:
            return float(lat), float(lng)
    if isinstance(coordinates, (list, tuple)) and len(coordinates) >= 2:
        return float(coordinates[1]), float(coordinates[0])
    return None, None
