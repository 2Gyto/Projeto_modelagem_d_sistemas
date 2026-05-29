"""Endpoints públicos (sem autenticação) — fluxo do usuário final."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.simulacao_publica_service import SimulacaoPublicaService
from app.domain.exceptions import EntityNotFoundError
from app.infrastructure.db.session import get_db
from app.infrastructure.http.schemas import (
    SimulacaoPublicaCreate,
    SimulacaoPublicaResponse,
)

router = APIRouter(prefix="/simulacoes/publica", tags=["Simulação Pública"])


def get_service(db: Session = Depends(get_db)) -> SimulacaoPublicaService:
    return SimulacaoPublicaService(db)


@router.post(
    "",
    response_model=SimulacaoPublicaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_simulacao_publica(
    body: SimulacaoPublicaCreate,
    service: SimulacaoPublicaService = Depends(get_service),
) -> SimulacaoPublicaResponse:
    return service.executar(body)


@router.get("/{simulacao_id}", response_model=SimulacaoPublicaResponse)
def obter_simulacao_publica(
    simulacao_id: uuid.UUID,
    service: SimulacaoPublicaService = Depends(get_service),
) -> SimulacaoPublicaResponse:
    try:
        return service.obter(simulacao_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
