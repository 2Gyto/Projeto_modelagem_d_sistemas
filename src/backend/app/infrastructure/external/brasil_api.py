from app.config import get_settings
from app.infrastructure.external.base_client import BaseHttpClient

_settings = get_settings()


class BrasilApiClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("Brasil API", _settings.brasil_api_base_url)

    async def buscar_cep(self, cep: str) -> dict:
        cep_limpo = "".join(c for c in cep if c.isdigit())
        response = await self.get(f"/cep/v2/{cep_limpo}")
        return response.json()
