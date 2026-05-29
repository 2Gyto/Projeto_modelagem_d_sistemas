"""Testes das rotas de simulação com SimulacaoService mockado."""

from __future__ import annotations

import uuid
from unittest.mock import MagicMock

import pytest

from app.application.simulacao_service import SimulacaoService
from app.domain.exceptions import DomainError, EntityNotFoundError
from app.domain.enums import StatusSimulacao
from app.infrastructure.db.models import Simulacao, Usuario
from app.infrastructure.http.routers import simulacoes as simulacoes_router


def _simulacao_payload() -> dict:
    return {
        "consumo_kwh": "350.50",
        "tipo_entrada": "KWH",
        "cep": "01310100",
        "cidade": "São Paulo",
        "area_m2": "45.00",
        "orientacao": "NORTE",
        "tipo_conexao": "MONOFASICA",
    }


@pytest.fixture
def sim_service_mock() -> MagicMock:
    return MagicMock(spec=SimulacaoService)


class TestSimulacoesRouter:
    def test_criar_simulacao_201(
        self,
        client_authenticated,
        usuario: Usuario,
        simulacao: Simulacao,
        sim_service_mock: MagicMock,
    ) -> None:
        # Objetivo: POST /simulacoes persiste rascunho e retorna SimulacaoResponse.
        sim_service_mock.criar_rascunho.return_value = simulacao

        from app.main import app

        app.dependency_overrides[simulacoes_router.get_simulacao_service] = (
            lambda: sim_service_mock
        )
        try:
            response = client_authenticated.post(
                "/api/v1/simulacoes",
                json=_simulacao_payload(),
            )
        finally:
            app.dependency_overrides.pop(
                simulacoes_router.get_simulacao_service, None
            )

        assert response.status_code == 201
        body = response.json()
        assert body["id"] == str(simulacao.id)
        assert body["status"] == StatusSimulacao.INICIADA.value
        sim_service_mock.criar_rascunho.assert_called_once()

    def test_criar_simulacao_422_regra_negocio(
        self,
        client_authenticated,
        sim_service_mock: MagicMock,
    ) -> None:
        # Objetivo: DomainError (RB01) vira 422 na API.
        sim_service_mock.criar_rascunho.side_effect = DomainError(
            "Informe consumo em kWh ou valor em reais (RB01)."
        )

        from app.main import app

        app.dependency_overrides[simulacoes_router.get_simulacao_service] = (
            lambda: sim_service_mock
        )
        try:
            response = client_authenticated.post(
                "/api/v1/simulacoes",
                json=_simulacao_payload(),
            )
        finally:
            app.dependency_overrides.pop(
                simulacoes_router.get_simulacao_service, None
            )

        assert response.status_code == 422

    def test_listar_simulacoes_200(
        self,
        client_authenticated,
        simulacao: Simulacao,
        sim_service_mock: MagicMock,
        usuario: Usuario,
    ) -> None:
        # Objetivo: GET /simulacoes lista histórico do usuário logado.
        sim_service_mock.listar_do_usuario.return_value = [simulacao]

        from app.main import app

        app.dependency_overrides[simulacoes_router.get_simulacao_service] = (
            lambda: sim_service_mock
        )
        try:
            response = client_authenticated.get("/api/v1/simulacoes")
        finally:
            app.dependency_overrides.pop(
                simulacoes_router.get_simulacao_service, None
            )

        assert response.status_code == 200
        assert len(response.json()) == 1
        sim_service_mock.listar_do_usuario.assert_called_once_with(usuario.id)

    def test_obter_simulacao_404(
        self,
        client_authenticated,
        sim_service_mock: MagicMock,
    ) -> None:
        # Objetivo: simulação inexistente retorna 404.
        sim_service_mock.obter.side_effect = EntityNotFoundError(
            "Simulação não encontrada."
        )
        sim_id = uuid.uuid4()

        from app.main import app

        app.dependency_overrides[simulacoes_router.get_simulacao_service] = (
            lambda: sim_service_mock
        )
        try:
            response = client_authenticated.get(f"/api/v1/simulacoes/{sim_id}")
        finally:
            app.dependency_overrides.pop(
                simulacoes_router.get_simulacao_service, None
            )

        assert response.status_code == 404

    def test_executar_simulacao_501_placeholder(
        self,
        client_authenticated,
        simulacao: Simulacao,
        sim_service_mock: MagicMock,
    ) -> None:
        # Objetivo: motor de cálculo ainda não implementado — contrato 501.
        sim_service_mock.obter.return_value = simulacao

        from app.main import app

        app.dependency_overrides[simulacoes_router.get_simulacao_service] = (
            lambda: sim_service_mock
        )
        try:
            response = client_authenticated.post(
                f"/api/v1/simulacoes/{simulacao.id}/executar"
            )
        finally:
            app.dependency_overrides.pop(
                simulacoes_router.get_simulacao_service, None
            )

        assert response.status_code == 501
        assert "próxima etapa" in response.json()["detail"].lower()

    def test_criar_simulacao_401_sem_autenticacao(self, client) -> None:
        # Objetivo: endpoint exige usuário autenticado.
        response = client.post("/api/v1/simulacoes", json=_simulacao_payload())
        assert response.status_code == 401

    def test_obter_simulacao_200(
        self,
        client_authenticated,
        simulacao: Simulacao,
        sim_service_mock: MagicMock,
    ) -> None:
        # Objetivo: GET /simulacoes/{id} retorna detalhe quando o registro existe.
        sim_service_mock.obter.return_value = simulacao

        from app.main import app

        app.dependency_overrides[simulacoes_router.get_simulacao_service] = (
            lambda: sim_service_mock
        )
        try:
            response = client_authenticated.get(
                f"/api/v1/simulacoes/{simulacao.id}"
            )
        finally:
            app.dependency_overrides.pop(
                simulacoes_router.get_simulacao_service, None
            )

        assert response.status_code == 200
        assert response.json()["id"] == str(simulacao.id)

    def test_executar_simulacao_404_quando_inexistente(
        self,
        client_authenticated,
        sim_service_mock: MagicMock,
    ) -> None:
        # Objetivo: executar simulação inexistente retorna 404 antes do 501.
        sim_service_mock.obter.side_effect = EntityNotFoundError(
            "Simulação não encontrada."
        )
        sim_id = uuid.uuid4()

        from app.main import app

        app.dependency_overrides[simulacoes_router.get_simulacao_service] = (
            lambda: sim_service_mock
        )
        try:
            response = client_authenticated.post(
                f"/api/v1/simulacoes/{sim_id}/executar"
            )
        finally:
            app.dependency_overrides.pop(
                simulacoes_router.get_simulacao_service, None
            )

        assert response.status_code == 404
