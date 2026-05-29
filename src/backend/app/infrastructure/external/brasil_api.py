import logging
from decimal import Decimal, InvalidOperation

from app.config import get_settings

logger = logging.getLogger(__name__)
from app.domain.exceptions import DomainError, ExternalApiError
from app.infrastructure.external.base_client import BaseHttpClient
from app.infrastructure.external.dtos import CoordenadasCep

_settings = get_settings()


class BrasilApiClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("Brasil API", _settings.brasil_api_base_url)

    async def buscar_cep(self, cep: str) -> dict:
        cep_limpo = "".join(c for c in cep if c.isdigit())
        response = await self.get(f"/cep/v2/{cep_limpo}")
        return response.json()

    async def resolver_coordenadas(self, cep: str) -> CoordenadasCep:
        """RB02 — CEP → latitude, longitude e UF."""
        if not cep or len("".join(c for c in cep if c.isdigit())) != 8:
            raise DomainError("CEP inválido. Informe 8 dígitos (RB02).")

        payload = await self.buscar_cep(cep)
        location = payload.get("location") or {}
        coordinates = location.get("coordinates") or {}

        lat_raw = coordinates.get("latitude")
        lon_raw = coordinates.get("longitude")
        if lat_raw is None or lon_raw is None:
            cep_limpo = "".join(c for c in cep if c.isdigit())
            logger.warning(
                "Brasil API: CEP %s sem coordenadas (location.coordinates ausente ou incompleto)",
                cep_limpo,
            )
            raise ExternalApiError(
                "Brasil API",
                "Coordenadas geográficas não retornadas para o CEP informado.",
            )

        try:
            latitude = Decimal(str(lat_raw))
            longitude = Decimal(str(lon_raw))
        except (InvalidOperation, TypeError) as exc:
            raise ExternalApiError(
                "Brasil API",
                "Coordenadas geográficas inválidas para o CEP informado.",
            ) from exc

        estado = payload.get("state")
        if not estado:
            raise ExternalApiError(
                "Brasil API",
                "Estado (UF) não retornado para o CEP informado.",
            )

        cidade = payload.get("city") or payload.get("cidade") or ""
        cep_limpo = "".join(c for c in cep if c.isdigit())

        return CoordenadasCep(
            cep=cep_limpo,
            latitude=latitude,
            longitude=longitude,
            estado=str(estado).upper(),
            cidade=str(cidade),
        )
