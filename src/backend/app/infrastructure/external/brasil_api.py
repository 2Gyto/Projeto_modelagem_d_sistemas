from dataclasses import dataclass
from decimal import Decimal

import httpx

from app.config import get_settings
from app.domain.exceptions import DomainError, ExternalApiError
from app.infrastructure.external.base_client import BaseHttpClient

_settings = get_settings()


@dataclass(frozen=True)
class CepGeolocalizacao:
    cep: str
    uf: str
    cidade: str
    latitude: Decimal
    longitude: Decimal


class BrasilApiClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("Brasil API", _settings.brasil_api_base_url)

    async def buscar_cep_v2(self, cep: str) -> CepGeolocalizacao:
        cep_limpo = "".join(c for c in cep if c.isdigit())
        if len(cep_limpo) != 8:
            raise DomainError("CEP inválido. Informe 8 dígitos. (RB02)")

        url = f"{self.base_url}/cep/v2/{cep_limpo}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
        except httpx.TimeoutException as exc:
            raise ExternalApiError(
                self.api_name,
                "Serviço temporariamente indisponível. Tente novamente mais tarde.",
            ) from exc
        except httpx.HTTPError as exc:
            raise ExternalApiError(
                self.api_name, "Não foi possível consultar o CEP."
            ) from exc

        if response.status_code == 404:
            raise DomainError("CEP não encontrado. Verifique e tente novamente. (RB02)")
        if response.status_code >= 400:
            raise ExternalApiError(
                self.api_name, "Falha ao consultar o CEP."
            )

        data = response.json()
        uf = (data.get("state") or "").strip().upper()
        cidade = (data.get("city") or "").strip()
        coords = (data.get("location") or {}).get("coordinates") or {}

        try:
            lat = Decimal(str(coords.get("latitude")))
            lon = Decimal(str(coords.get("longitude")))
        except Exception as exc:
            raise DomainError(
                "CEP sem coordenadas geográficas. Não é possível simular. (RB02)"
            ) from exc

        if not uf:
            raise DomainError("Não foi possível identificar o estado (UF) do CEP. (RB02)")

        return CepGeolocalizacao(
            cep=cep_limpo,
            uf=uf,
            cidade=cidade,
            latitude=lat,
            longitude=lon,
        )
