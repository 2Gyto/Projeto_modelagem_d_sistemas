from fastapi import APIRouter

from app.config import get_settings
from app.infrastructure.http.schemas import HealthResponse

router = APIRouter(tags=["Sistema"])
_settings = get_settings()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", app=_settings.app_name)
