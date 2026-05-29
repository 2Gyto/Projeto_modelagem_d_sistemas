"""Orquestração da simulação — cálculo completo virá nas próximas iterações."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

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
    Simulacao,
    Usuario,
)
from app.infrastructure.http.schemas import SimulacaoCreate


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
            raise DomainError("Enum de entrada inválido.") from exc

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
                cep=dados.cep,
                cidade=dados.cidade,
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

    def listar_do_usuario(self, usuario_id: uuid.UUID) -> list[Simulacao]:
        stmt = (
            select(Simulacao)
            .where(Simulacao.usuario_id == usuario_id)
            .order_by(Simulacao.realizada_em.desc())
        )
        return list(self._db.scalars(stmt).all())

    def obter(self, usuario_id: uuid.UUID, simulacao_id: uuid.UUID) -> Simulacao:
        sim = self._db.get(Simulacao, simulacao_id)
        if not sim or sim.usuario_id != usuario_id:
            raise EntityNotFoundError("Simulação não encontrada.")
        return sim
