"""Testes da dependência get_current_user (autenticação Bearer)."""

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.application.auth_service import AuthService
from app.application.security import create_access_token
from app.domain.exceptions import EntityNotFoundError
from app.infrastructure.http.dependencies import get_current_user


class TestGetCurrentUser:
    def test_rejeita_ausencia_de_token(self) -> None:
        # Objetivo: rotas protegidas exigem Authorization header.
        auth = MagicMock(spec=AuthService)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(None, auth)

        assert exc_info.value.status_code == 401
        assert "ausente" in exc_info.value.detail.lower()

    def test_rejeita_token_invalido(self, usuario) -> None:
        # Objetivo: JWT adulterado não autentica.
        creds = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="token.invalido",
        )
        auth = MagicMock(spec=AuthService)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(creds, auth)

        assert exc_info.value.status_code == 401

    def test_rejeita_sub_uuid_invalido(self) -> None:
        # Edge case: subject do JWT não é UUID válido.
        token = create_access_token("nao-e-uuid")
        creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        auth = MagicMock(spec=AuthService)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(creds, auth)

        assert "inválido" in exc_info.value.detail.lower()

    def test_retorna_usuario_quando_token_valido(self, usuario) -> None:
        # Objetivo: caminho feliz resolve usuário via AuthService.
        token = create_access_token(str(usuario.id))
        creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        auth = MagicMock(spec=AuthService)
        auth.get_user.return_value = usuario

        result = get_current_user(creds, auth)

        assert result is usuario
        auth.get_user.assert_called_once_with(usuario.id)

    def test_rejeita_quando_usuario_nao_existe_no_banco(self, usuario) -> None:
        # Objetivo: token válido mas usuário removido retorna 401.
        token = create_access_token(str(usuario.id))
        creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        auth = MagicMock(spec=AuthService)
        auth.get_user.side_effect = EntityNotFoundError("Usuário não encontrado.")

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(creds, auth)

        assert exc_info.value.status_code == 401
