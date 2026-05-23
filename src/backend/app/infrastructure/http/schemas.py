import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field

from app.domain.enums import StatusSimulacao


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)


class UsuarioResponse(BaseModel):
    id: uuid.UUID
    nome: str
    email: str
    criado_em: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SimulacaoCreate(BaseModel):
    """Entrada mínima para iniciar uma simulação (RF01–RF04)."""

    consumo_kwh: Decimal | None = Field(default=None, gt=0)
    valor_reais: Decimal | None = Field(default=None, gt=0)
    tipo_entrada: str
    cep: str | None = Field(default=None, min_length=8, max_length=9)
    cidade: str | None = None
    area_m2: Decimal = Field(gt=0)
    orientacao: str
    tipo_conexao: str
    concessionaria: str | None = None


class SimulacaoResponse(BaseModel):
    id: uuid.UUID
    status: StatusSimulacao
    realizada_em: datetime

    model_config = {"from_attributes": True}


class HealthResponse(BaseModel):
    status: str
    app: str


class SimulacaoTesteRequest(BaseModel):
    nome: str
    cep: str
    gasto: str
    tipo: str


class HspPorCepRequest(BaseModel):
    cep: str = Field(min_length=8, max_length=9)


class HspPorCepResponse(BaseModel):
    cep: str
    uf: str
    cidade: str
    latitude: float
    longitude: float
    hsp_mensal: dict[str, float] = Field(
        description="Média diária de HSP por mês (chave YYYYMM → h/dia)."
    )
    hsp_medio_anual: float = Field(
        description="Média das médias mensais (h/dia) no ano de referência."
    )
    ano_referencia: int