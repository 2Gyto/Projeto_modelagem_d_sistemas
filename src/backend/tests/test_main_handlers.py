"""Testes dos exception handlers globais registrados em main.py."""

import json

import pytest

from app.domain.exceptions import DomainError, ExternalApiError
from app.main import domain_error_handler, external_api_handler


class TestExceptionHandlers:
    @pytest.mark.asyncio
    async def test_domain_error_handler_retorna_422(self) -> None:
        # Objetivo: erros de negócio não viram 500 genérico.
        response = await domain_error_handler(None, DomainError("falha RB"))
        assert response.status_code == 422
        assert json.loads(response.body) == {"detail": "falha RB"}

    @pytest.mark.asyncio
    async def test_external_api_handler_retorna_503_com_api_name(self) -> None:
        # Objetivo: integrações externas expõem nome da API no JSON (ADR-03).
        exc = ExternalApiError("Brasil API", "timeout")
        response = await external_api_handler(None, exc)
        assert response.status_code == 503
        body = json.loads(response.body)
        assert body["api"] == "Brasil API"
        assert "timeout" in body["detail"]
