from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.domain.exceptions import DomainError, ExternalApiError
from app.infrastructure.http.routers import (
    auth,
    health,
    simulacao_publica,
    simulacoes,
)

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


_prefix = _settings.api_prefix
app.include_router(health.router, prefix=_prefix)
app.include_router(auth.router, prefix=_prefix)
app.include_router(simulacoes.router, prefix=_prefix)
app.include_router(simulacao_publica.router, prefix=_prefix)


_FRONT_DIR = Path(__file__).resolve().parents[2] / "front_solarcalc"
_STATIC_DIR = _FRONT_DIR / "static"
_TEMPLATES_DIR = _FRONT_DIR / "templates"

if _STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    return FileResponse(_TEMPLATES_DIR / "index.html")


@app.get("/dashboard", include_in_schema=False)
def serve_dashboard() -> FileResponse:
    return FileResponse(_TEMPLATES_DIR / "dashboard.html")
