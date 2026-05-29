from decimal import Decimal
from statistics import mean

from app.config import get_settings
from app.domain.exceptions import DomainError, ExternalApiError
from app.infrastructure.external.base_client import BaseHttpClient
from app.infrastructure.external.dtos import IndiceIrradiacao

_settings = get_settings()


class NasaPowerClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("NASA POWER", _settings.nasa_power_base_url)

    async def buscar_irradiacao_mensal(
        self, latitude: float, longitude: float
    ) -> dict:
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

    async def obter_hsp(self, latitude: Decimal, longitude: Decimal) -> IndiceIrradiacao:
        """RB03 — média mensal de ALLSKY_SFC_SW_DWN (kWh/m²/dia) ≈ HSP."""
        payload = await self.buscar_irradiacao_mensal(
            float(latitude), float(longitude)
        )
        try:
            serie = payload["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
            valores = [
                float(v)
                for v in serie.values()
                if v is not None and float(v) > 0
            ]
        except (KeyError, TypeError, ValueError) as exc:
            raise ExternalApiError(
                "NASA POWER",
                "Formato de irradiação solar não reconhecido.",
            ) from exc

        if not valores:
            raise DomainError(
                "Dados de irradiação indisponíveis para a localização (RB03)."
            )

        hsp = Decimal(str(round(mean(valores), 2)))
        if hsp <= 0:
            raise DomainError("Índice HSP inválido para a região (RB03).")

        return IndiceIrradiacao(hsp=hsp)
