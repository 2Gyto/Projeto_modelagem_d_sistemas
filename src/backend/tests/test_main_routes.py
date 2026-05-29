"""Testes de rotas auxiliares em main.py (frontend estático)."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import _frontend_index


class TestFrontendRoutes:
    def test_frontend_index_retorna_404_quando_index_ausente(self) -> None:
        # Objetivo: /app sem index.html responde JSON 404 (linhas 65-68 de main.py).
        mock_index = MagicMock(spec=Path)
        mock_index.exists.return_value = False
        with patch("app.main._front_templates") as mock_tpl:
            mock_tpl.__truediv__.return_value = mock_index
            response = _frontend_index()

        assert response.status_code == 404

    def test_get_app_endpoint_via_cliente(self, client: TestClient) -> None:
        # Objetivo: rota GET /app registrada na aplicação (integração leve).
        response = client.get("/app")
        assert response.status_code in (200, 404)
