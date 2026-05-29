"""Integração AuthService + rotas HTTP + persistência real."""

from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.auth_service import AuthService
from app.application.security import decode_access_token
from app.domain.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.infrastructure.db.models import Usuario


pytestmark = pytest.mark.integration


class TestAuthServiceIntegration:
    def test_register_persiste_e_normaliza_email(
        self, db_session: Session
    ) -> None:
        service = AuthService(db_session)
        user = service.register("Maria", "  MARIA@Example.COM  ", "senha12345")

        assert user.email == "maria@example.com"
        stored = db_session.scalar(
            select(Usuario).where(Usuario.email == "maria@example.com")
        )
        assert stored is not None
        assert stored.id == user.id

    def test_register_duplicado_lanca_domain_error(
        self, db_session: Session
    ) -> None:
        service = AuthService(db_session)
        service.register("A", "dup@test.com", "senha12345")

        with pytest.raises(EmailAlreadyRegisteredError):
            service.register("B", "dup@test.com", "senha12345")

    def test_login_retorna_token_valido(self, db_session: Session) -> None:
        service = AuthService(db_session)
        service.register("João", "joao@test.com", "senha12345")

        user, token = service.login("joao@test.com", "senha12345")
        assert decode_access_token(token) == str(user.id)

    def test_login_senha_errada(self, db_session: Session) -> None:
        service = AuthService(db_session)
        service.register("João", "joao@test.com", "senha12345")

        with pytest.raises(InvalidCredentialsError):
            service.login("joao@test.com", "senha_errada")

    def test_get_user_inexistente(self, db_session: Session) -> None:
        from app.domain.exceptions import EntityNotFoundError

        with pytest.raises(EntityNotFoundError):
            AuthService(db_session).get_user(uuid.uuid4())


class TestAuthHttpIntegration:
    def test_fluxo_register_login_me(
        self, integration_client: TestClient
    ) -> None:
        reg = integration_client.post(
            "/api/v1/auth/register",
            json={
                "nome": "Fluxo E2E",
                "email": "fluxo@example.com",
                "senha": "senha12345",
            },
        )
        assert reg.status_code == 201
        user_id = reg.json()["id"]

        login = integration_client.post(
            "/api/v1/auth/login",
            json={"email": "fluxo@example.com", "senha": "senha12345"},
        )
        assert login.status_code == 200
        token = login.json()["access_token"]

        me = integration_client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me.status_code == 200
        assert me.json()["id"] == user_id

    def test_me_sem_token_retorna_401(
        self, integration_client: TestClient
    ) -> None:
        response = integration_client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_register_email_duplicado_retorna_409(
        self, integration_client: TestClient
    ) -> None:
        payload = {
            "nome": "Dup",
            "email": "dup409@example.com",
            "senha": "senha12345",
        }
        assert integration_client.post("/api/v1/auth/register", json=payload).status_code == 201
        second = integration_client.post("/api/v1/auth/register", json=payload)
        assert second.status_code == 409
