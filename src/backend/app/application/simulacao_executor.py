import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.application.calculo_fotovoltaico import CalculoFotovoltaicoService, EntradaCalculo
from app.config import get_settings
from app.domain.enums import StatusSimulacao, TipoEntradaConsumo
from app.domain.exceptions import DomainError, EntityNotFoundError
from app.infrastructure.db.models import (
    DadosConsumo,
    DadosTelhado,
    Localizacao,
    ProjecaoAnual,
    Resultado,
    Simulacao,
)
from app.infrastructure.db.tarifa_sqlite import TarifaSqliteRepository
from app.infrastructure.external.brasil_api import BrasilApiClient
from app.infrastructure.external.nasa_power import NasaPowerClient


class SimulacaoExecutor:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._settings = get_settings()
        self._brasil = BrasilApiClient()
        self._nasa = NasaPowerClient()
        self._tarifas = TarifaSqliteRepository()
        self._calculo = CalculoFotovoltaicoService(self._settings)

    async def executar(self, usuario_id: uuid.UUID, simulacao_id: uuid.UUID) -> Simulacao:
        sim = self._db.get(Simulacao, simulacao_id)
        if not sim or sim.usuario_id != usuario_id:
            raise EntityNotFoundError("Simulação não encontrada.")

        consumo_row = sim.dados_consumo
        loc_row = sim.localizacao
        telhado_row = sim.dados_telhado

        if not consumo_row or not loc_row or not telhado_row:
            raise DomainError("Simulação incompleta. Recrie o rascunho.")

        if not loc_row.cep:
            raise DomainError("CEP é obrigatório para a simulação. (RB02)")

        sim.status = StatusSimulacao.VALIDANDO_DADOS
        self._db.flush()

        geo = await self._brasil.buscar_cep_v2(loc_row.cep)
        loc_row.uf = geo.uf
        loc_row.cidade = geo.cidade
        loc_row.latitude = geo.latitude
        loc_row.longitude = geo.longitude

        tarifa = self._tarifas.por_uf(geo.uf)
        loc_row.tarifa_kwh_usada = tarifa.tarifa_kwh

        sim.status = StatusSimulacao.BUSCANDO_IRRADIACAO
        self._db.flush()

        hsp = await self._nasa.buscar_hsp_medio_dia(geo.latitude, geo.longitude)
        loc_row.hsp_medio_dia = hsp

        consumo_kwh = self._resolver_consumo_kwh(consumo_row, tarifa.tarifa_kwh)
        consumo_row.consumo_kwh = consumo_kwh

        sim.status = StatusSimulacao.CALCULANDO
        self._db.flush()

        try:
            resultado_calc = self._calculo.calcular(
                EntradaCalculo(
                    consumo_kwh_mes=consumo_kwh,
                    area_m2=telhado_row.area_m2,
                    orientacao=telhado_row.orientacao,
                    tipo_conexao=telhado_row.tipo_conexao,
                    hsp_medio_dia=hsp,
                    tarifa=tarifa,
                )
            )
        except ValueError as exc:
            raise DomainError(str(exc)) from exc

        if sim.resultado:
            self._db.delete(sim.resultado)
            self._db.flush()

        resultado = Resultado(
            simulacao_id=sim.id,
            geracao_kwh=resultado_calc.geracao_kwh_mes,
            potencia_kwp=resultado_calc.potencia_kwp,
            qtd_paineis=resultado_calc.qtd_paineis,
            economia_mensal=resultado_calc.economia_mensal,
            payback_anos=Decimal(resultado_calc.payback_anos),
            payback_meses=Decimal(resultado_calc.payback_meses),
            custo_total=resultado_calc.investimento,
            lucro_25_anos=resultado_calc.lucro_25_anos,
            ano_payback=resultado_calc.ano_payback,
        )
        self._db.add(resultado)
        self._db.flush()

        for proj in resultado_calc.projecoes:
            self._db.add(
                ProjecaoAnual(
                    resultado_id=resultado.id,
                    ano=proj.ano,
                    custo_concessionaria=proj.custo_concessionaria,
                    custo_fotovoltaico=proj.custo_fotovoltaico,
                    saldo=proj.custo_concessionaria - proj.custo_fotovoltaico,
                )
            )

        sim.status = StatusSimulacao.CONCLUIDA
        self._db.commit()
        self._db.refresh(sim)
        return sim

    @staticmethod
    def _resolver_consumo_kwh(consumo_row: DadosConsumo, tarifa_kwh: Decimal) -> Decimal:
        if consumo_row.tipo_entrada == TipoEntradaConsumo.KWH:
            if consumo_row.consumo_kwh is None or consumo_row.consumo_kwh <= 0:
                raise DomainError("Consumo em kWh inválido. (RB01)")
            return consumo_row.consumo_kwh
        if consumo_row.valor_reais is None or consumo_row.valor_reais <= 0:
            raise DomainError("Valor em reais inválido. (RB01)")
        return (consumo_row.valor_reais / tarifa_kwh).quantize(Decimal("0.01"))
