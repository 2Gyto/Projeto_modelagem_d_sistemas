"""Testes das rotas de autenticação com AuthService mockado via banco."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from app.application.auth_service import AuthService
from app.domain.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError
from app.infrastructure.db.models import Usuario
from app.infrastructure.http.dependencies import get_auth_service


@pytest.fixture
def auth_service_mock(mock_db: MagicMock) -> MagicMock:
    """AuthService real sobre sessão mock — permite patch de métodos."""
    return MagicMock(spec=AuthService)


class TestAuthRouterRegister:
    def test_register_201_quando_sucesso(
        self, client, auth_service_mock: MagicMock
    ) -> None:
        # Objetivo: cadastro retorna 201 e corpo UsuarioResponse.
        novo = Usuario(
            id=uuid.uuid4(),
            nome="Ana",
            email="ana@example.com",
            senha_hash="hash",
            criado_em=datetime.now(timezone.utc),
        )
        auth_service_mock.register.return_value = novo

        def _override() -> MagicMock:
            return auth_service_mock

        from app.main import app

        app.dependency_overrides[get_auth_service] = _override
        try:
            response = client.post(
                "/api/v1/auth/register",
                json={
                    "nome": "Ana",
                    "email": "ana@example.com",
                    "senha": "senha12345",
                },
            )
        finally:
            app.dependency_overrides.pop(get_auth_service, None)

        assert response.status_code == 201
        assert response.json()["email"] == "ana@example.com"

    def test_register_409_email_duplicado(
        self, client, auth_service_mock: MagicMock
    ) -> None:
        # Objetivo: conflito de e-mail vira HTTP 409, não 500.
        auth_service_mock.register.side_effect = EmailAlreadyRegisteredError(
            "E-mail já cadastrado."
        )

        from app.main import app

        app.dependency_overrides[get_auth_service] = lambda: auth_service_mock
        try:
            response = client.post(
                "/api/v1/auth/register",
                json={
                    "nome": "Ana",
                    "email": "dup@example.com",
                    "senha": "senha12345",
                },
            )
        finally:
            app.dependency_overrides.pop(get_auth_service, None)

        assert response.status_code == 409


class TestAuthRouterLogin:
    def test_login_200_retorna_token(self, client, auth_service_mock: MagicMock) -> None:
        # Objetivo: login bem-sucedido expõe access_token bearer.
        user = Usuario(
            id=uuid.uuid4(),
            nome="U",
            email="u@e.com",
            senha_hash="h",
            criado_em=datetime.now(timezone.utc),
        )
        auth_service_mock.login.return_value = (user, "jwt-token-fake")

        from app.main import app

        app.dependency_overrides[get_auth_service] = lambda: auth_service_mock
        try:
            response = client.post(
                "/api/v1/auth/login",
                json={"email": "u@e.com", "senha": "senha12345"},
            )
        finally:
            app.dependency_overrides.pop(get_auth_service, None)

        assert response.status_code == 200
        body = response.json()
        assert body["access_token"] == "jwt-token-fake"
        assert body["token_type"] == "bearer"

    def test_login_401_credenciais_invalidas(
        self, client, auth_service_mock: MagicMock
    ) -> None:
        # Objetivo: falha de autenticação não vaza detalhes internos.
        auth_service_mock.login.side_effect = InvalidCredentialsError(
            "E-mail ou senha inválidos."
        )

        from app.main import app

        app.dependency_overrides[get_auth_service] = lambda: auth_service_mock
        try:
            response = client.post(
                "/api/v1/auth/login",
                json={"email": "u@e.com", "senha": "errada"},
            )
        finally:
            app.dependency_overrides.pop(get_auth_service, None)

        assert response.status_code == 401


class TestAuthRouterMe:
    def test_me_retorna_usuario_autenticado(
        self, client_authenticated, usuario: Usuario
    ) -> None:
        # Objetivo: /me devolve perfil do usuário injetado pela dependência.
        response = client_authenticated.get("/api/v1/auth/me")
        assert response.status_code == 200
        assert response.json()["id"] == str(usuario.id)
        assert response.json()["email"] == usuario.email
