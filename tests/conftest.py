"""Fixtures globais para testes de integração — banco real (SQLite), HTTP e fakes de hardware."""

from __future__ import annotations

import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Garante import de `app` e `scripts` a partir de src/backend
_BACKEND_ROOT = Path(__file__).resolve().parents[1] / "src" / "backend"
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.config import get_settings
from app.infrastructure.db.session import get_db
from app.infrastructure.db.testing import (
    create_test_engine,
    create_test_session_factory,
    file_database_url,
    reset_database,
)
from app.main import app


@pytest.fixture(autouse=True)
def _integration_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Settings determinísticos; nunca usa PostgreSQL de produção."""
    monkeypatch.setenv("JWT_SECRET", "integration-test-secret-key-32chars-min")
    monkeypatch.setenv("JWT_EXPIRE_MINUTES", "60")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv(
        "DATABASE_URL",
        "sqlite+pysqlite:///:memory:",
    )
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
    app.dependency_overrides.clear()


@pytest.fixture
def integration_engine(tmp_path: Path):
    """Engine SQLite com schema completo; arquivo em tmp_path evita estado entre testes."""
    db_file = tmp_path / "integration.db"
    engine = create_test_engine(file_database_url(db_file))
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(integration_engine) -> Generator[Session, None, None]:
    """Sessão SQLAlchemy real com rollback implícito via reset entre testes."""
    factory = create_test_session_factory(integration_engine)
    session = factory()
    try:
        yield session
    finally:
        session.close()
        reset_database(integration_engine)


@pytest.fixture
def integration_client(integration_engine) -> Generator[TestClient, None, None]:
    """TestClient com get_db apontando para SQLite — sem mock de Session."""
    factory = create_test_session_factory(integration_engine)

    def _override_get_db() -> Generator[Session, None, None]:
        db = factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def auth_token(integration_client: TestClient) -> str:
    """Registra usuário padrão e retorna JWT válido."""
    integration_client.post(
        "/api/v1/auth/register",
        json={
            "nome": "Integração Teste",
            "email": "integracao@example.com",
            "senha": "senha12345",
        },
    )
    login = integration_client.post(
        "/api/v1/auth/login",
        json={"email": "integracao@example.com", "senha": "senha12345"},
    )
    assert login.status_code == 200
    return login.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def simulacao_payload() -> dict:
    return {
        "consumo_kwh": "350.50",
        "valor_reais": None,
        "tipo_entrada": "KWH",
        "cep": "01310100",
        "cidade": "São Paulo",
        "area_m2": "45.00",
        "orientacao": "NORTE",
        "tipo_conexao": "MONOFASICA",
    }
