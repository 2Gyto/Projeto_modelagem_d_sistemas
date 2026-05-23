import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.irradiacao_service import IrradiacaoService
from app.application.simulacao_service import SimulacaoService
from app.domain.exceptions import DomainError, EntityNotFoundError
from app.infrastructure.db.models import Usuario
from app.infrastructure.db.session import get_db
from app.infrastructure.http.dependencies import get_current_user
from app.infrastructure.http.schemas import (
    HspPorCepRequest,
    HspPorCepResponse,
    SimulacaoCreate,
    SimulacaoResponse,
    SimulacaoTesteRequest,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/simulacoes", tags=["Simulações"])


def get_simulacao_service(db: Session = Depends(get_db)) -> SimulacaoService:
    return SimulacaoService(db)


def get_irradiacao_service() -> IrradiacaoService:
    return IrradiacaoService()


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


@router.get("/{simulacao_id}", response_model=SimulacaoResponse)
def obter_simulacao(
    simulacao_id: uuid.UUID,
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> SimulacaoResponse:
    try:
        sim = service.obter(user.id, simulacao_id)
        return SimulacaoResponse.model_validate(sim)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("/{simulacao_id}/executar")
def executar_simulacao(
    simulacao_id: uuid.UUID,
    user: Usuario = Depends(get_current_user),
    service: SimulacaoService = Depends(get_simulacao_service),
) -> SimulacaoResponse:
    """Placeholder: integra Brasil API, NASA POWER, Gemini e motor de cálculo."""
    try:
        service.obter(user.id, simulacao_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Motor de cálculo e integrações externas serão implementados na próxima etapa."
        ),
    )

@router.post("/hsp", response_model=HspPorCepResponse)
async def obter_hsp_por_cep(
    body: HspPorCepRequest,
    service: IrradiacaoService = Depends(get_irradiacao_service),
) -> HspPorCepResponse:
    """
    CEP → Brasil API (coordenadas) → NASA POWER → horas de pico de sol (HSP).
    """
    endereco, irradiacao = await service.obter_hsp_por_cep(body.cep)
    return HspPorCepResponse(
        cep=endereco.cep,
        uf=endereco.uf,
        cidade=endereco.cidade,
        latitude=endereco.latitude,
        longitude=endereco.longitude,
        hsp_mensal=irradiacao.hsp_mensal,
        hsp_medio_anual=irradiacao.hsp_medio,
        ano_referencia=irradiacao.ano_referencia,
    )


@router.post("/teste-integracao")
async def receber_dados_iniciais(
    dados: SimulacaoTesteRequest,
    service: IrradiacaoService = Depends(get_irradiacao_service),
):
    """
    Ponte com o front: CEP → Brasil API → SQLite (tarifa/UF) → NASA POWER (HSP mensal).
    """
    endereco, irradiacao, tarifa = await service.preparar_dados_por_cep(dados.cep)

    return {
        "status": "sucesso",
        "mensagem": (
            f"Dados recebidos, {dados.nome}. "
            f"HSP e tarifa obtidos para {endereco.cidade}/{endereco.uf}."
        ),
        "nome": dados.nome,
        "gasto": dados.gasto,
        "tipo": dados.tipo,
        "uf": endereco.uf,
        "tarifa_kwh": float(tarifa),
        "localizacao": {
            "cep": endereco.cep,
            "uf": endereco.uf,
            "cidade": endereco.cidade,
            "latitude": endereco.latitude,
            "longitude": endereco.longitude,
        },
        "hsp_mensal": irradiacao.hsp_mensal,
        "hsp_medio_anual": irradiacao.hsp_medio,
        "ano_referencia": irradiacao.ano_referencia,
    }