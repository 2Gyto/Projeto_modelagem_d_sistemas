"""Testes do endpoint de saúde — sem dependência de banco."""

from app.config import get_settings


class TestHealthRouter:
    def test_health_retorna_ok(self, client) -> None:
        # Objetivo: monitoramento/load balancer verifica disponibilidade da API.
        settings = get_settings()
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["app"] == settings.app_name
