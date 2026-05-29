"""Fixtures compartilhadas — sessão mockada, usuário de teste e cliente HTTP."""

from __future__ import annotations

import uuid
from collections.abc import Generator
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.application.security import create_access_token, hash_password
from app.config import get_settings
from app.domain.enums import StatusSimulacao
from app.infrastructure.db.models import Simulacao, Usuario
from app.infrastructure.db.session import get_db
from app.infrastructure.http.dependencies import get_current_user
from app.infrastructure.http.schemas import SimulacaoCreate
from app.main import app


@pytest.fixture(autouse=True)
def _reset_settings_cache(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Garante JWT e demais settings previsíveis em cada teste."""
    monkeypatch.setenv("JWT_SECRET", "test-secret-key-unit-tests-only-32chars")
    monkeypatch.setenv("JWT_EXPIRE_MINUTES", "60")
    monkeypatch.setenv("DEBUG", "true")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def mock_db() -> MagicMock:
    """Sessão SQLAlchemy mockada — evita PostgreSQL real nos testes unitários."""
    return MagicMock(spec=Session)


@pytest.fixture
def usuario() -> Usuario:
    """Usuário autenticável com id fixo para asserts determinísticos."""
    return Usuario(
        id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
        nome="Usuário Teste",
        email="teste@example.com",
        senha_hash=hash_password("senha12345"),
        criado_em=datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc),
    )


@pytest.fixture
def simulacao(usuario: Usuario) -> Simulacao:
    """Simulação pertencente ao usuário de teste."""
    return Simulacao(
        id=uuid.UUID("22222222-2222-2222-2222-222222222222"),
        usuario_id=usuario.id,
        status=StatusSimulacao.INICIADA,
        realizada_em=datetime(2026, 3, 1, 10, 0, tzinfo=timezone.utc),
    )


@pytest.fixture
def simulacao_create_payload() -> SimulacaoCreate:
    """Payload válido mínimo para criar rascunho (RF01–RF04)."""
    return SimulacaoCreate(
        consumo_kwh=Decimal("350.50"),
        valor_reais=None,
        tipo_entrada="KWH",
        cep="01310100",
        cidade="São Paulo",
        area_m2=Decimal("45.00"),
        orientacao="NORTE",
        tipo_conexao="MONOFASICA",
    )


@pytest.fixture
def auth_headers(usuario: Usuario) -> dict[str, str]:
    """Header Bearer com JWT válido para rotas protegidas."""
    token = create_access_token(str(usuario.id))
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def override_db(mock_db: MagicMock) -> Generator[MagicMock, None, None]:
    """Substitui get_db pela sessão mockada."""

    def _get_db() -> Generator[MagicMock, None, None]:
        yield mock_db

    app.dependency_overrides[get_db] = _get_db
    yield mock_db
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def override_current_user(usuario: Usuario) -> Generator[Usuario, None, None]:
    """Bypass de autenticação JWT — foco no comportamento das rotas de simulação."""

    app.dependency_overrides[get_current_user] = lambda: usuario
    yield usuario
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def client(override_db: MagicMock) -> Generator[TestClient, None, None]:
    """Cliente HTTP contra a app FastAPI com banco mockado."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def client_authenticated(
    client: TestClient,
    override_current_user: Usuario,
) -> TestClient:
    """Cliente com usuário já injetado nas dependências."""
    return client
