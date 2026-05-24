import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.application.simulacao_executor import SimulacaoExecutor
from app.domain.enums import (
    OrientacaoTelhado,
    StatusSimulacao,
    TipoConexao,
    TipoEntradaConsumo,
)
from app.domain.exceptions import DomainError, EntityNotFoundError
from app.infrastructure.db.models import (
    DadosConsumo,
    DadosTelhado,
    Localizacao,
    Resultado,
    Simulacao,
    Usuario,
)
from app.infrastructure.http.schemas import (
    LocalizacaoResponse,
    ProjecaoAnualResponse,
    ResultadoDetalheResponse,
    SimulacaoCreate,
    SimulacaoDetalheResponse,
    TelhadoResponse,
)


class SimulacaoService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def criar_rascunho(self, usuario: Usuario, dados: SimulacaoCreate) -> Simulacao:
        if dados.consumo_kwh is None and dados.valor_reais is None:
            raise DomainError("Informe consumo em kWh ou valor em reais (RB01).")

        try:
            tipo_entrada = TipoEntradaConsumo(dados.tipo_entrada.upper())
            orientacao = OrientacaoTelhado(dados.orientacao.upper())
            tipo_conexao = TipoConexao(dados.tipo_conexao.upper())
        except ValueError as exc:
            raise DomainError("Valor de enum inválido.") from exc

        sim = Simulacao(usuario_id=usuario.id, status=StatusSimulacao.INICIADA)
        self._db.add(sim)
        self._db.flush()

        self._db.add(
            DadosConsumo(
                simulacao_id=sim.id,
                consumo_kwh=dados.consumo_kwh,
                valor_reais=dados.valor_reais,
                tipo_entrada=tipo_entrada,
            )
        )
        self._db.add(
            Localizacao(
                simulacao_id=sim.id,
                cep="".join(c for c in dados.cep if c.isdigit()),
            )
        )
        self._db.add(
            DadosTelhado(
                simulacao_id=sim.id,
                area_m2=dados.area_m2,
                orientacao=orientacao,
                tipo_conexao=tipo_conexao,
            )
        )
        self._db.commit()
        self._db.refresh(sim)
        return sim

    async def criar_e_executar(
        self, usuario: Usuario, dados: SimulacaoCreate
    ) -> Simulacao:
        sim = self.criar_rascunho(usuario, dados)
        executor = SimulacaoExecutor(self._db)
        return await executor.executar(usuario.id, sim.id)

    async def executar(self, usuario_id: uuid.UUID, simulacao_id: uuid.UUID) -> Simulacao:
        executor = SimulacaoExecutor(self._db)
        return await executor.executar(usuario_id, simulacao_id)

    def listar_do_usuario(self, usuario_id: uuid.UUID) -> list[Simulacao]:
        stmt = (
            select(Simulacao)
            .where(Simulacao.usuario_id == usuario_id)
            .order_by(Simulacao.realizada_em.desc())
        )
        return list(self._db.scalars(stmt).all())

    def obter_detalhe(
        self, usuario_id: uuid.UUID, simulacao_id: uuid.UUID
    ) -> SimulacaoDetalheResponse:
        stmt = (
            select(Simulacao)
            .where(
                Simulacao.id == simulacao_id,
                Simulacao.usuario_id == usuario_id,
            )
            .options(
                joinedload(Simulacao.localizacao),
                joinedload(Simulacao.dados_consumo),
                joinedload(Simulacao.dados_telhado),
                joinedload(Simulacao.resultado).joinedload(Resultado.projecoes),
            )
        )
        sim = self._db.scalars(stmt).first()
        if not sim:
            raise EntityNotFoundError("Simulação não encontrada.")
        return self._to_detalhe(sim)

    @staticmethod
    def _to_detalhe(sim: Simulacao) -> SimulacaoDetalheResponse:
        loc_resp = None
        if sim.localizacao:
            loc = sim.localizacao
            loc_resp = LocalizacaoResponse(
                cep=loc.cep,
                uf=loc.uf,
                cidade=loc.cidade,
                latitude=loc.latitude,
                longitude=loc.longitude,
                hsp_medio_dia=loc.hsp_medio_dia,
                tarifa_kwh=loc.tarifa_kwh_usada,
            )

        res_resp = None
        if sim.resultado:
            r = sim.resultado
            anos = int(r.payback_anos or 0)
            meses = int(r.payback_meses or 0)
            payback_texto = (
                f"{anos} ano(s) e {meses} mês(es)"
                if meses
                else f"{anos} ano(s)"
            )
            projecoes = sorted(r.projecoes, key=lambda p: p.ano)
            consumo_kwh = (
                sim.dados_consumo.consumo_kwh if sim.dados_consumo else None
            )

            from app.config import get_settings

            res_resp = ResultadoDetalheResponse(
                geracao_kwh_mes=r.geracao_kwh,
                potencia_kwp=r.potencia_kwp,
                qtd_paineis=r.qtd_paineis,
                economia_mensal=r.economia_mensal,
                investimento=r.custo_total,
                payback_anos=anos,
                payback_meses=meses,
                payback_texto=payback_texto,
                lucro_25_anos=r.lucro_25_anos,
                ano_payback=r.ano_payback,
                marcas=get_settings().marcas_paineis,
                consumo_kwh_mes=consumo_kwh,
                projecoes=[
                    ProjecaoAnualResponse(
                        ano=p.ano,
                        custo_concessionaria=p.custo_concessionaria,
                        custo_fotovoltaico=p.custo_fotovoltaico,
                    )
                    for p in projecoes
                ],
            )

        tel_resp = None
        if sim.dados_telhado:
            t = sim.dados_telhado
            tel_resp = TelhadoResponse(
                area_m2=t.area_m2,
                orientacao=t.orientacao.value,
                tipo_conexao=t.tipo_conexao.value,
            )

        return SimulacaoDetalheResponse(
            id=sim.id,
            status=sim.status,
            realizada_em=sim.realizada_em,
            localizacao=loc_resp,
            telhado=tel_resp,
            resultado=res_resp,
        )
