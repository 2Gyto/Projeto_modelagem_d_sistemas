import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.simulacao_service import SimulacaoService
from app.domain.exceptions import DomainError, EntityNotFoundError
from app.infrastructure.db.models import Usuario
from app.infrastructure.db.session import get_db
from app.infrastructure.http.dependencies import get_current_user
from app.infrastructure.http.schemas import (
    SimulacaoCompletaCreate,
    SimulacaoCreate,
    SimulacaoDetalheResponse,
    SimulacaoResponse,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/simulacoes", tags=["Simulações"])


def get_simulacao_service(db: Session = Depends(get_db)) -> SimulacaoService:
    return SimulacaoService(db)


@router.post("", response_model=SimulacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_simulacao(
    body: SimulacaoCreate,
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> SimulacaoResponse:
    try:
        sim = service.criar_rascunho(user, body)
        return SimulacaoResponse.model_validate(sim)
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/completa",
    response_model=SimulacaoDetalheResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_simulacao_completa(
    body: SimulacaoCompletaCreate,
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> SimulacaoDetalheResponse:
    """Cria rascunho e executa pipeline Brasil API → tarifa UF → NASA → cálculo."""
    try:
        sim = await service.criar_e_executar(user, body)
        return service.obter_detalhe(user.id, sim.id)
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[SimulacaoResponse])
def listar_simulacoes(
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> list[SimulacaoResponse]:
    sims = service.listar_do_usuario(user.id)
    return [SimulacaoResponse.model_validate(s) for s in sims]


@router.get("/{simulacao_id}", response_model=SimulacaoDetalheResponse)
def obter_simulacao(
    simulacao_id: uuid.UUID,
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> SimulacaoDetalheResponse:
    try:
        return service.obter_detalhe(user.id, simulacao_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("/{simulacao_id}/executar", response_model=SimulacaoDetalheResponse)
async def executar_simulacao(
    simulacao_id: uuid.UUID,
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> SimulacaoDetalheResponse:
    try:
        await service.executar(user.id, simulacao_id)
        return service.obter_detalhe(user.id, simulacao_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
