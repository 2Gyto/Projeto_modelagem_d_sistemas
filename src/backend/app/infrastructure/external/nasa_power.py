from datetime import date

from app.config import get_settings
from app.domain.exceptions import DomainError
from app.domain.geo import DadosIrradiacao
from app.infrastructure.external.base_client import BaseHttpClient

_settings = get_settings()

# Irradiação global horizontal (Wh/m²/dia) — base para HSP
_PARAMETRO_IRRADIACAO = "ALLSKY_SFC_SW_DWN"
# 1 h de sol pleno ≈ 1 kWh/m² → Wh/m²/dia ÷ 1000 = horas de pico/dia
_WH_POR_HORA_PICO = 1000.0


class NasaPowerClient(BaseHttpClient):
    def __init__(self) -> None:
        super().__init__("NASA POWER", _settings.nasa_power_base_url)

    async def buscar_hsp(self, latitude: float, longitude: float) -> DadosIrradiacao:
        """
        Consulta irradiação mensal nas coordenadas e devolve horas de pico de sol (HSP).

        A NASA retorna ALLSKY_SFC_SW_DWN em Wh/m²/dia (média diária do mês).
        HSP do mês = valor / 1000. HSP médio anual = média dos meses válidos.
        """
        ano = date.today().year - 1
        path = (
            "/temporal/monthly/point"
            f"?parameters={_PARAMETRO_IRRADIACAO}"
            f"&community=RE"
            f"&latitude={latitude}"
            f"&longitude={longitude}"
            f"&start={ano}0101"
            f"&end={ano}1231"
            f"&format=JSON"
        )
        response = await self.get(path)
        return _parsear_hsp(response.json(), ano_referencia=ano)


def _parsear_hsp(payload: dict, ano_referencia: int) -> DadosIrradiacao:
    try:
        serie = payload["properties"]["parameter"][_PARAMETRO_IRRADIACAO]
    except (KeyError, TypeError) as exc:
        raise DomainError(
            "Resposta da NASA POWER sem dados de irradiação solar."
        ) from exc

    hsp_mensal: dict[str, float] = {}
    valores: list[float] = []

    for chave, wh_m2_dia in serie.items():
        if wh_m2_dia is None or wh_m2_dia <= 0:
            continue
        hsp_dia = round(float(wh_m2_dia) / _WH_POR_HORA_PICO, 3)
        hsp_mensal[str(chave)] = hsp_dia
        valores.append(hsp_dia)

    if not valores:
        raise DomainError(
            "Sem dados de irradiação solar para estas coordenadas (RB03)."
        )

    hsp_medio = round(sum(valores) / len(valores), 2)
    return DadosIrradiacao(
        hsp_medio=hsp_medio,
        hsp_mensal=hsp_mensal,
        ano_referencia=ano_referencia,
    )
