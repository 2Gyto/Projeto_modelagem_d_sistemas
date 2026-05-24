from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.domain.exceptions import DomainError, ExternalApiError
from app.infrastructure.http.routers import auth, health, simulacoes

_settings = get_settings()

app = FastAPI(
    title=_settings.app_name,
    version="0.1.0",
    description="API REST do simulador SolarCalc (monólito em camadas — ADR-02).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(ExternalApiError)
async def external_api_handler(_: Request, exc: ExternalApiError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": str(exc),
            "api": exc.api_name,
        },
    )


@app.on_event("startup")
def garantir_tarifas_sqlite() -> None:
    import sys

    db_path = Path(_settings.tarifas_sqlite_path)
    if not db_path.exists():
        backend_root = Path(__file__).resolve().parents[1]
        if str(backend_root) not in sys.path:
            sys.path.insert(0, str(backend_root))
        from scripts.seed_tarifas_uf import main as seed_tarifas

        seed_tarifas()


_prefix = _settings.api_prefix
app.include_router(health.router, prefix=_prefix)
app.include_router(auth.router, prefix=_prefix)
app.include_router(simulacoes.router, prefix=_prefix)

_front = Path(__file__).resolve().parents[2] / "front_solarcalc"
if _front.is_dir():
    app.mount("/app", StaticFiles(directory=str(_front), html=True), name="frontend")
