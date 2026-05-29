"""Testes das funções puras de hash e JWT (camada application/security)."""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from jose import jwt

from app.application.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.config import get_settings


class TestPasswordHashing:
    def test_hash_password_gera_hash_diferente_do_plaintext(self) -> None:
        # Objetivo: garantir que senhas nunca são armazenadas em texto claro.
        plain = "minha_senha_segura"
        hashed = hash_password(plain)
        assert hashed != plain
        assert hashed.startswith("$2b$")

    def test_verify_password_aceita_senha_correta(self) -> None:
        # Objetivo: fluxo de login depende de verificação bcrypt bem-sucedida.
        plain = "senha12345"
        hashed = hash_password(plain)
        assert verify_password(plain, hashed) is True

    def test_verify_password_rejeita_senha_incorreta(self) -> None:
        # Objetivo: credenciais inválidas não devem passar na verificação.
        hashed = hash_password("senha_correta")
        assert verify_password("senha_errada", hashed) is False

    def test_verify_password_rejeita_hash_vazio(self) -> None:
        # Edge case: hash ausente não deve autenticar nem propagar exceção interna.
        assert verify_password("qualquer", "") is False

    def test_verify_password_rejeita_hash_malformado(self) -> None:
        # Edge case: hash inválido retorna False em vez de UnknownHashError (login seguro).
        assert verify_password("qualquer", "nao-e-bcrypt") is False


class TestJwtTokens:
    def test_create_and_decode_roundtrip(self) -> None:
        # Objetivo: token emitido no login deve ser decodificável com o mesmo segredo.
        subject = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        token = create_access_token(subject)
        assert decode_access_token(token) == subject

    def test_decode_retorna_none_para_token_invalido(self) -> None:
        # Objetivo: tokens adulterados não autenticam (proteção contra tampering).
        assert decode_access_token("token.invalido.xyz") is None

    def test_decode_retorna_none_para_token_expirado(self) -> None:
        # Objetivo: tokens expirados são rejeitados (RB de sessão).
        settings = get_settings()
        expired = datetime.now(timezone.utc) - timedelta(minutes=1)
        payload = {"sub": "user-id", "exp": expired}
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        assert decode_access_token(token) is None

    def test_decode_retorna_none_quando_sub_ausente(self) -> None:
        # Edge case: payload sem subject não identifica usuário.
        settings = get_settings()
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
        token = jwt.encode(
            {"exp": expire},
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        assert decode_access_token(token) is None

    def test_create_access_token_respeita_expiracao_configurada(self) -> None:
        # Objetivo: expiração segue Settings.jwt_expire_minutes.
        settings = get_settings()
        with patch("app.application.security._settings", settings):
            before = datetime.now(timezone.utc)
            token = create_access_token("user-1")
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
            exp = payload["exp"]
            if isinstance(exp, datetime):
                exp_dt = exp
            else:
                exp_dt = datetime.fromtimestamp(exp, tz=timezone.utc)
            delta_minutes = (exp_dt - before).total_seconds() / 60
            assert 55 <= delta_minutes <= settings.jwt_expire_minutes + 5
