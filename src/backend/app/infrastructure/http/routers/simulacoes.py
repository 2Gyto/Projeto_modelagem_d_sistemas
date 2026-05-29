import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from app.application.email_service import enviar_email_simulacao
from app.application.simulacao_service import SimulacaoService
from app.domain.enums import StatusSimulacao
from app.domain.exceptions import DomainError, EntityNotFoundError
from app.infrastructure.db.models import Usuario
from app.infrastructure.db.session import get_db
from app.infrastructure.http.dependencies import get_current_user
from app.infrastructure.http.schemas import (
    SimulacaoCreate,
    SimulacaoResponse,
    SimulacaoResultadoResponse,
    SimulacaoTesteRequest,
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


@router.get("", response_model=list[SimulacaoResponse])
def listar_simulacoes(
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> list[SimulacaoResponse]:
    sims = service.listar_do_usuario(user.id)
    return [SimulacaoResponse.model_validate(s) for s in sims]


@router.get("/{simulacao_id}", response_model=SimulacaoResultadoResponse)
def obter_simulacao(
    simulacao_id: uuid.UUID,
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> SimulacaoResultadoResponse:
    try:
        sim = service.obter(user.id, simulacao_id)
        if sim.status != StatusSimulacao.CONCLUIDA or not sim.resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resultado da simulação ainda não disponível.",
            )
        return SimulacaoResultadoResponse.from_simulacao(sim)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/{simulacao_id}/executar",
    response_model=SimulacaoResultadoResponse,
    status_code=status.HTTP_200_OK,
)
async def executar_simulacao(
    simulacao_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> SimulacaoResultadoResponse:
    """
    Micro-etapa C: pipeline com Brasil API, tarifas por UF, NASA POWER e Gemini.
    """
    try:
        execucao = await service.executar(user.id, simulacao_id)
        background_tasks.add_task(
            enviar_email_simulacao,
            user.email,
            str(simulacao_id),
            execucao.payback_texto,
        )
        return SimulacaoResultadoResponse.from_simulacao(execucao.simulacao)
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


@router.post("/teste-integracao")
async def receber_dados_iniciais(dados: SimulacaoTesteRequest):
    """
    Fase 1: Rota temporária para validar a ponte com o Front-end.
    """
    print("--- NOVA INTEGRAÇÃO RECEBIDA ---")
    print(f"Usuário: {dados.nome}")
    print(f"CEP: {dados.cep}")
    print(f"Gasto Mensal: {dados.gasto}")
    print(f"Tipo: {dados.tipo}")
    print("--------------------------------")

    return {
        "status": "sucesso",
        "mensagem": (
            f"Dados recebidos perfeitamente, {dados.nome}! A ponte Front-Back está viva."
        ),
    }
