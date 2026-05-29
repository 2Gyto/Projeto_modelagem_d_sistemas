"""Testes de factories de dependência nos routers."""

from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.application.auth_service import AuthService
from app.application.simulacao_service import SimulacaoService
from app.infrastructure.http.dependencies import get_auth_service
from app.infrastructure.http.routers.simulacoes import get_simulacao_service


class TestRouterFactories:
    def test_get_auth_service_instancia_com_sessao(self) -> None:
        # Objetivo: factory de auth injeta Session no AuthService.
        db = MagicMock(spec=Session)
        service = get_auth_service(db)
        assert isinstance(service, AuthService)
        assert service._db is db

    def test_get_simulacao_service_instancia_com_sessao(self) -> None:
        # Objetivo: factory de simulação segue o mesmo padrão de injeção.
        db = MagicMock(spec=Session)
        service = get_simulacao_service(db)
        assert isinstance(service, SimulacaoService)
        assert service._db is db
