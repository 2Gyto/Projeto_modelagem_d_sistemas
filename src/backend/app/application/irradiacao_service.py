from decimal import Decimal

from app.domain.geo import DadosIrradiacao, EnderecoGeo
from app.infrastructure.db.tarifa_uf import TarifaUfRepository
from app.infrastructure.external.brasil_api import BrasilApiClient
from app.infrastructure.external.nasa_power import NasaPowerClient


class IrradiacaoService:
    """CEP → Brasil API → NASA POWER; tarifa por UF no SQLite."""

    def __init__(self) -> None:
        self._brasil = BrasilApiClient()
        self._nasa = NasaPowerClient()
        self._tarifas = TarifaUfRepository()

    async def obter_hsp_por_cep(self, cep: str) -> tuple[EnderecoGeo, DadosIrradiacao]:
        endereco = await self._brasil.resolver_cep(cep)
        irradiacao = await self._nasa.buscar_hsp(
            endereco.latitude,
            endereco.longitude,
        )
        return endereco, irradiacao

    async def preparar_dados_por_cep(
        self, cep: str
    ) -> tuple[EnderecoGeo, DadosIrradiacao, Decimal]:
        endereco, irradiacao = await self.obter_hsp_por_cep(cep)
        tarifa = self._tarifas.buscar_por_uf(endereco.uf)
        return endereco, irradiacao, tarifa
