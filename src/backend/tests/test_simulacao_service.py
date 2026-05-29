"""Testes unitários do SimulacaoService — regras RB01 e enums."""

from __future__ import annotations

import uuid
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.application.simulacao_service import SimulacaoService
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


def _payload(**kwargs) -> SimulacaoCreate:
    base = {
        "consumo_kwh": Decimal("200"),
        "valor_reais": None,
        "tipo_entrada": "KWH",
        "cep": "30130010",
        "cidade": "Belo Horizonte",
        "area_m2": Decimal("30"),
        "orientacao": "SUL",
        "tipo_conexao": "BIFASICA",
    }
    base.update(kwargs)
    return SimulacaoCreate(**base)


class TestSimulacaoServiceCriarRascunho:
    def test_criar_rascunho_persiste_entidades_relacionadas(
        self,
        mock_db: MagicMock,
        usuario: Usuario,
        simulacao_create_payload: SimulacaoCreate,
    ) -> None:
        # Objetivo: caminho feliz cria Simulacao + consumo + localização + telhado.
        added: list[object] = []
        mock_db.add.side_effect = lambda obj: added.append(obj)

        service = SimulacaoService(mock_db)
        result = service.criar_rascunho(usuario, simulacao_create_payload)

        assert len(added) == 4
        assert isinstance(added[0], Simulacao)
        assert added[0].status == StatusSimulacao.INICIADA
        assert added[0].usuario_id == usuario.id

        consumo = next(o for o in added if isinstance(o, DadosConsumo))
        assert consumo.tipo_entrada == TipoEntradaConsumo.KWH
        assert consumo.consumo_kwh == simulacao_create_payload.consumo_kwh

        loc = next(o for o in added if isinstance(o, Localizacao))
        assert loc.cep == simulacao_create_payload.cep
        assert loc.cidade == simulacao_create_payload.cidade

        telhado = next(o for o in added if isinstance(o, DadosTelhado))
        assert telhado.orientacao == OrientacaoTelhado.NORTE
        assert telhado.tipo_conexao == TipoConexao.MONOFASICA

        mock_db.flush.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(result)

    def test_criar_rascunho_aceita_valor_reais_sem_kwh(
        self, mock_db: MagicMock, usuario: Usuario
    ) -> None:
        # Objetivo: RB01 permite entrada por valor em reais (RF01).
        payload = _payload(
            consumo_kwh=None,
            valor_reais=Decimal("450.00"),
            tipo_entrada="REAIS",
        )
        added: list[object] = []
        mock_db.add.side_effect = lambda obj: added.append(obj)

        SimulacaoService(mock_db).criar_rascunho(usuario, payload)

        consumo = next(o for o in added if isinstance(o, DadosConsumo))
        assert consumo.tipo_entrada == TipoEntradaConsumo.REAIS
        assert consumo.valor_reais == Decimal("450.00")

    def test_criar_rascunho_rejeita_sem_consumo_nem_valor(
        self, mock_db: MagicMock, usuario: Usuario
    ) -> None:
        # Objetivo: RB01 — ao menos um indicador de consumo é obrigatório.
        payload = _payload(consumo_kwh=None, valor_reais=None)

        with pytest.raises(DomainError, match="RB01"):
            SimulacaoService(mock_db).criar_rascunho(usuario, payload)

        mock_db.add.assert_not_called()

    def test_criar_rascunho_rejeita_enum_invalido(
        self, mock_db: MagicMock, usuario: Usuario
    ) -> None:
        # Objetivo: enums desconhecidos não chegam ao banco.
        payload = _payload(tipo_entrada="INVALIDO")

        with pytest.raises(DomainError, match="Enum"):
            SimulacaoService(mock_db).criar_rascunho(usuario, payload)

    def test_criar_rascunho_normaliza_enums_maiusculas(
        self, mock_db: MagicMock, usuario: Usuario
    ) -> None:
        # Edge case: entrada em minúsculas é convertida via .upper().
        payload = _payload(
            tipo_entrada="kwh",
            orientacao="leste",
            tipo_conexao="trifasica",
        )
        added: list[object] = []
        mock_db.add.side_effect = lambda obj: added.append(obj)

        SimulacaoService(mock_db).criar_rascunho(usuario, payload)

        telhado = next(o for o in added if isinstance(o, DadosTelhado))
        assert telhado.orientacao == OrientacaoTelhado.LESTE
        assert telhado.tipo_conexao == TipoConexao.TRIFASICA


class TestSimulacaoServiceConsultas:
    def test_listar_do_usuario_retorna_lista_ordenada(
        self, mock_db: MagicMock, simulacao: Simulacao
    ) -> None:
        # Objetivo: histórico de simulações do usuário autenticado.
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [simulacao]
        mock_db.scalars.return_value = mock_scalars

        resultado = SimulacaoService(mock_db).listar_do_usuario(simulacao.usuario_id)

        assert resultado == [simulacao]
        mock_db.scalars.assert_called_once()

    def test_listar_do_usuario_retorna_vazio(
        self, mock_db: MagicMock, usuario: Usuario
    ) -> None:
        # Edge case: usuário sem simulações anteriores.
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_db.scalars.return_value = mock_scalars

        assert SimulacaoService(mock_db).listar_do_usuario(usuario.id) == []

    def test_obter_retorna_simulacao_do_proprio_usuario(
        self, mock_db: MagicMock, usuario: Usuario, simulacao: Simulacao
    ) -> None:
        # Objetivo: detalhe acessível apenas ao dono do registro.
        mock_db.get.return_value = simulacao

        found = SimulacaoService(mock_db).obter(usuario.id, simulacao.id)
        assert found is simulacao

    def test_obter_lanca_quando_nao_existe(self, mock_db: MagicMock, usuario: Usuario) -> None:
        # Objetivo: ID inexistente retorna 404 na camada HTTP.
        mock_db.get.return_value = None

        with pytest.raises(EntityNotFoundError):
            SimulacaoService(mock_db).obter(usuario.id, uuid.uuid4())

    def test_obter_lanca_quando_simulacao_de_outro_usuario(
        self, mock_db: MagicMock, simulacao: Simulacao
    ) -> None:
        # Objetivo: isolamento entre usuários — não vazar simulação alheia.
        mock_db.get.return_value = simulacao
        outro_id = uuid.UUID("99999999-9999-9999-9999-999999999999")

        with pytest.raises(EntityNotFoundError):
            SimulacaoService(mock_db).obter(outro_id, simulacao.id)
