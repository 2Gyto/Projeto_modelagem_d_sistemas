"""Integração de rotas estáticas, health e handlers globais de erro."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


pytestmark = pytest.mark.integration


class TestHealthIntegration:
    def test_health_retorna_ok(self, integration_client: TestClient) -> None:
        r = integration_client.get("/api/v1/health")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "ok"
        assert "SolarCalc" in body["app"]


class TestFrontendIntegration:
    def test_app_index_disponivel(self, integration_client: TestClient) -> None:
        r = integration_client.get("/app")
        assert r.status_code == 200

    def test_static_css_disponivel(self, integration_client: TestClient) -> None:
        r = integration_client.get("/static/css/style.css")
        assert r.status_code == 200
