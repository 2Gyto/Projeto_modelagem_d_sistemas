from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< Updated upstream
from fastapi.responses import JSONResponse
=======
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
>>>>>>> Stashed changes

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


_prefix = _settings.api_prefix
app.include_router(health.router, prefix=_prefix)
app.include_router(auth.router, prefix=_prefix)
app.include_router(simulacoes.router, prefix=_prefix)
<<<<<<< Updated upstream
=======

# Servir frontend estático: templates em /app e assets estáticos em /static
_front = Path(__file__).resolve().parents[2] / "front_solarcalc"
_front_templates = _front / "templates"
_front_static = _front / "static"
if _front_templates.is_dir():
    app.mount("/app", StaticFiles(directory=str(_front_templates), html=True), name="frontend")
if _front_static.is_dir():
    app.mount("/static", StaticFiles(directory=str(_front_static)), name="static")


@app.get("/app", include_in_schema=False)
def _frontend_index():
    index_path = _front_templates / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return JSONResponse(status_code=404, content={"detail": "Not found"})
>>>>>>> Stashed changes
