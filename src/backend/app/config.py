from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "SolarCalc API"
    debug: bool = False
    api_prefix: str = "/api/v1"

    database_url: str = (
        "postgresql+psycopg://solarcalc:solarcalc@localhost:5432/solarcalc"
    )

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24

    external_api_timeout_seconds: float = 10.0

    brasil_api_base_url: str = "https://brasilapi.com.br/api"
    nasa_power_base_url: str = "https://power.larc.nasa.gov/api"
    gemini_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
