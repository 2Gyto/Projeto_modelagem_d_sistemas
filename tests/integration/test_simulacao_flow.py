"""Integração SimulacaoService + FKs + isolamento entre usuários."""

from __future__ import annotations

import uuid
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.application.auth_service import AuthService
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
)
from app.infrastructure.http.schemas import SimulacaoCreate


pytestmark = pytest.mark.integration


def _criar_usuario(db: Session, email: str) -> object:
    return AuthService(db).register("Teste", email, "senha12345")


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


class TestSimulacaoServiceIntegration:
    def test_criar_rascunho_persiste_relacionamentos(
        self, db_session: Session
    ) -> None:
        user = _criar_usuario(db_session, "sim1@test.com")
        service = SimulacaoService(db_session)
        sim = service.criar_rascunho(user, _payload())

        loaded = db_session.scalar(
            select(Simulacao)
            .where(Simulacao.id == sim.id)
            .options(
                selectinload(Simulacao.dados_consumo),
                selectinload(Simulacao.localizacao),
                selectinload(Simulacao.dados_telhado),
            )
        )
        assert loaded is not None
        assert loaded.status == StatusSimulacao.INICIADA
        assert loaded.dados_consumo is not None
        assert loaded.dados_consumo.tipo_entrada == TipoEntradaConsumo.KWH
        assert loaded.localizacao is not None
        assert loaded.localizacao.cep == "30130010"
        assert loaded.dados_telhado is not None
        assert loaded.dados_telhado.orientacao == OrientacaoTelhado.SUL
        assert loaded.dados_telhado.tipo_conexao == TipoConexao.BIFASICA

    def test_rb01_sem_consumo_nao_persiste(
        self, db_session: Session
    ) -> None:
        user = _criar_usuario(db_session, "sim2@test.com")
        count_before = len(db_session.scalars(select(Simulacao)).all())

        with pytest.raises(DomainError):
            SimulacaoService(db_session).criar_rascunho(
                user,
                _payload(consumo_kwh=None, valor_reais=None),
            )

        db_session.expire_all()
        assert len(db_session.scalars(select(Simulacao)).all()) == count_before

    def test_isolamento_entre_usuarios(self, db_session: Session) -> None:
        u1 = _criar_usuario(db_session, "owner@test.com")
        u2 = _criar_usuario(db_session, "other@test.com")
        service = SimulacaoService(db_session)
        sim = service.criar_rascunho(u1, _payload())

        with pytest.raises(EntityNotFoundError):
            service.obter(u2.id, sim.id)


class TestSimulacaoHttpIntegration:
    def test_criar_listar_obter(
        self,
        integration_client: TestClient,
        auth_headers: dict[str, str],
        simulacao_payload: dict,
    ) -> None:
        create = integration_client.post(
            "/api/v1/simulacoes",
            json=simulacao_payload,
            headers=auth_headers,
        )
        assert create.status_code == 201
        sim_id = create.json()["id"]
        assert create.json()["status"] == "INICIADA"

        lista = integration_client.get(
            "/api/v1/simulacoes",
            headers=auth_headers,
        )
        assert lista.status_code == 200
        ids = [s["id"] for s in lista.json()]
        assert sim_id in ids

        detail = integration_client.get(
            f"/api/v1/simulacoes/{sim_id}",
            headers=auth_headers,
        )
        assert detail.status_code == 200

    def test_usuario_b_nao_acessa_simulacao_de_a(
        self,
        integration_client: TestClient,
        auth_headers: dict[str, str],
        simulacao_payload: dict,
    ) -> None:
        created = integration_client.post(
            "/api/v1/simulacoes",
            json=simulacao_payload,
            headers=auth_headers,
        )
        sim_id = created.json()["id"]

        integration_client.post(
            "/api/v1/auth/register",
            json={
                "nome": "Outro",
                "email": "outro@example.com",
                "senha": "senha12345",
            },
        )
        login_b = integration_client.post(
            "/api/v1/auth/login",
            json={"email": "outro@example.com", "senha": "senha12345"},
        )
        headers_b = {
            "Authorization": f"Bearer {login_b.json()['access_token']}"
        }

        forbidden = integration_client.get(
            f"/api/v1/simulacoes/{sim_id}",
            headers=headers_b,
        )
        assert forbidden.status_code == 404

    def test_executar_retorna_501_placeholder(
        self,
        integration_client: TestClient,
        auth_headers: dict[str, str],
        simulacao_payload: dict,
    ) -> None:
        sim_id = integration_client.post(
            "/api/v1/simulacoes",
            json=simulacao_payload,
            headers=auth_headers,
        ).json()["id"]

        exec_resp = integration_client.post(
            f"/api/v1/simulacoes/{sim_id}/executar",
            headers=auth_headers,
        )
        assert exec_resp.status_code == 501

    def test_payload_invalido_retorna_422(
        self,
        integration_client: TestClient,
        auth_headers: dict[str, str],
    ) -> None:
        response = integration_client.post(
            "/api/v1/simulacoes",
            json={
                "consumo_kwh": None,
                "valor_reais": None,
                "tipo_entrada": "KWH",
                "cep": "01310100",
                "area_m2": "10",
                "orientacao": "NORTE",
                "tipo_conexao": "MONOFASICA",
            },
            headers=auth_headers,
        )
        assert response.status_code == 422
