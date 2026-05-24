from decimal import Decimal

from app.config import get_settings
from app.domain.exceptions import DomainError, ExternalApiError
from app.infrastructure.external.base_client import BaseHttpClient

_settings = get_settings()
_MJ_PARA_KWH = Decimal("3.6")


class NasaPowerClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("NASA POWER", _settings.nasa_power_base_url)

    async def buscar_hsp_medio_dia(
        self, latitude: Decimal, longitude: Decimal
    ) -> Decimal:
        """HSP médio (horas de sol pico por dia) a partir de ALLSKY_SFC_SW_DWN mensal."""
        start = f"{_settings.nasa_start_year}01"
        end = f"{_settings.nasa_end_year}12"
        path = (
            "/temporal/monthly/point"
            f"?parameters=ALLSKY_SFC_SW_DWN"
            f"&community=RE"
            f"&latitude={float(latitude)}"
            f"&longitude={float(longitude)}"
            f"&start={start}&end={end}&format=JSON"
        )
        response = await self.get(path)
        data = response.json()

        try:
            serie = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
        except (KeyError, TypeError) as exc:
            raise DomainError(
                "Dados de irradiação indisponíveis para esta localização. (RB03)"
            ) from exc

        valores_validos: list[Decimal] = []
        for valor in serie.values():
            if valor is None or valor == -999:
                continue
            mj_dia = Decimal(str(valor))
            if mj_dia > 0:
                valores_validos.append(mj_dia / _MJ_PARA_KWH)

        if not valores_validos:
            raise DomainError(
                "Não foi possível calcular o HSP para esta região. (RB03)"
            )

        return sum(valores_validos) / len(valores_validos)
