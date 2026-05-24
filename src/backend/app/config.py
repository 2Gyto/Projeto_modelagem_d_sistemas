from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_ROOT = Path(__file__).resolve().parent.parent


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

    tarifas_sqlite_path: str = str(_BACKEND_ROOT / "data" / "tarifas_uf.db")

    # Motor de cálculo (valores médios de mercado — configuráveis)
    area_por_painel_m2: float = 1.7
    potencia_painel_kw: float = 0.55
    preco_painel_brl: float = 850.0
    eficiencia_sistema: float = 0.78
    inflacao_energia_anual: float = 0.05
    manutencao_anual_pct: float = 0.01
    anos_projecao: int = 25
    marcas_paineis: str = "Canadian Solar, Jinko Solar, Longi Solar"
    nasa_start_year: int = 2019
    nasa_end_year: int = 2023

    gemini_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
