"""Testes unitários do AuthService com sessão de banco mockada."""

from __future__ import annotations

import uuid
from unittest.mock import MagicMock

import pytest

from app.application.auth_service import AuthService
from app.application.security import hash_password, verify_password
from app.domain.exceptions import (
    EmailAlreadyRegisteredError,
    EntityNotFoundError,
    InvalidCredentialsError,
)
from app.infrastructure.db.models import Usuario


class TestAuthServiceRegister:
    def test_register_cria_usuario_quando_email_livre(self, mock_db: MagicMock) -> None:
        # Objetivo: caminho feliz de cadastro persiste usuário com e-mail normalizado.
        mock_db.scalar.return_value = None
        service = AuthService(mock_db)

        user = service.register("Maria Silva", "Maria@Example.COM", "senha12345")

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert user.email == "maria@example.com"
        assert user.nome == "Maria Silva"
        assert verify_password("senha12345", user.senha_hash)

    def test_register_rejeita_email_duplicado(self, mock_db: MagicMock) -> None:
        # Objetivo: RB de unicidade de e-mail — segundo cadastro falha (RF auth).
        existente = Usuario(
            id=uuid.uuid4(),
            nome="Outro",
            email="dup@example.com",
            senha_hash=hash_password("x"),
        )
        mock_db.scalar.return_value = existente
        service = AuthService(mock_db)

        with pytest.raises(EmailAlreadyRegisteredError, match="já cadastrado"):
            service.register("Novo", "dup@example.com", "senha12345")

        mock_db.add.assert_not_called()


class TestAuthServiceLogin:
    def test_login_retorna_usuario_e_token_valido(
        self, mock_db: MagicMock, usuario: Usuario
    ) -> None:
        # Objetivo: login bem-sucedido emite JWT utilizável.
        mock_db.scalar.return_value = usuario
        service = AuthService(mock_db)

        returned_user, token = service.login("teste@example.com", "senha12345")

        assert returned_user is usuario
        assert isinstance(token, str)
        assert len(token) > 20

    def test_login_normaliza_email(self, mock_db: MagicMock, usuario: Usuario) -> None:
        # Edge case: e-mail com maiúsculas e espaços deve encontrar o registro.
        mock_db.scalar.return_value = usuario
        service = AuthService(mock_db)

        service.login("  TESTE@EXAMPLE.COM  ", "senha12345")

        call_args = mock_db.scalar.call_args
        assert call_args is not None

    def test_login_falha_usuario_inexistente(self, mock_db: MagicMock) -> None:
        # Objetivo: não revelar se e-mail existe — mensagem genérica.
        mock_db.scalar.return_value = None
        service = AuthService(mock_db)

        with pytest.raises(InvalidCredentialsError):
            service.login("nao@existe.com", "senha12345")

    def test_login_falha_senha_incorreta(
        self, mock_db: MagicMock, usuario: Usuario
    ) -> None:
        # Objetivo: senha errada não autentica mesmo com usuário existente.
        mock_db.scalar.return_value = usuario
        service = AuthService(mock_db)

        with pytest.raises(InvalidCredentialsError):
            service.login("teste@example.com", "senha_errada")


class TestAuthServiceGetUser:
    def test_get_user_retorna_usuario_existente(
        self, mock_db: MagicMock, usuario: Usuario
    ) -> None:
        # Objetivo: recuperação por UUID para rotas autenticadas.
        mock_db.get.return_value = usuario
        service = AuthService(mock_db)

        found = service.get_user(usuario.id)
        assert found is usuario

    def test_get_user_lanca_quando_nao_encontrado(self, mock_db: MagicMock) -> None:
        # Objetivo: usuário removido após emissão do token não autentica.
        mock_db.get.return_value = None
        service = AuthService(mock_db)

        with pytest.raises(EntityNotFoundError, match="não encontrado"):
            service.get_user(uuid.uuid4())
