from pathlib import Path

from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _BACKEND_DIR.parent.parent
load_dotenv(_REPO_ROOT / ".env", override=True)
load_dotenv(_BACKEND_DIR / ".env", override=True)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.domain.exceptions import DomainError, ExternalApiError
from app.infrastructure.db import models  # noqa: F401 — registra metadados no Base
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.infrastructure.http.routers import auth, health, simulacoes

_settings = get_settings()

app = FastAPI(
    title=_settings.app_name,
    version="0.1.0",
    description="API REST do simulador SolarCalc (monólito em camadas — ADR-02).",
)

Base.metadata.create_all(bind=engine)

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


_prefix = _settings.api_prefix
app.include_router(health.router, prefix=_prefix)
app.include_router(auth.router, prefix=_prefix)
app.include_router(simulacoes.router, prefix=_prefix)

