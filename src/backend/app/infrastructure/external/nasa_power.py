from app.config import get_settings
from app.infrastructure.external.base_client import BaseHttpClient

_settings = get_settings()


class NasaPowerClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("NASA POWER", _settings.nasa_power_base_url)

    async def buscar_irradiacao_mensal(
        self, latitude: float, longitude: float
    ) -> dict:
        """Consulta irradiação — parâmetros finos serão ajustados na implementação."""
        path = (
            "/temporal/monthly/point"
            f"?parameters=ALLSKY_SFC_SW_DWN"
            f"&community=RE"
            f"&latitude={latitude}"
            f"&longitude={longitude}"
            f"&start=2020&end=2020&format=JSON"
        )
        response = await self.get(path)
        return response.json()
