"""Testes de configuração — Settings e cache lru."""

from app.config import Settings, get_settings


class TestSettings:
    def test_settings_valores_padrao(self) -> None:
        # Objetivo: contrato de configuração documentado no README.
        settings = Settings()
        assert settings.app_name == "SolarCalc API"
        assert settings.api_prefix == "/api/v1"
        assert settings.jwt_algorithm == "HS256"
        assert "postgresql" in settings.database_url

    def test_get_settings_usa_cache(self) -> None:
        # Objetivo: get_settings é singleton via lru_cache (performance).
        get_settings.cache_clear()
        first = get_settings()
        second = get_settings()
        assert first is second
        get_settings.cache_clear()
