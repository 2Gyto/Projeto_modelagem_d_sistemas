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


class SimulacaoPublicaCreate(BaseModel):
    """Entrada do fluxo público — apenas CEP + gasto + identificação do lead."""

    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    cep: str = Field(min_length=8, max_length=9)
    valor_reais: Decimal = Field(gt=0)


class SimulacaoPublicaResponse(BaseModel):
    simulacao_id: uuid.UUID
    nome: str
    email: str
    cep: str
    valor_reais: Decimal
    consumo_kwh_mes: Decimal
    quantidade_paineis: int
    potencia_sistema_kwp: Decimal
    geracao_total_kwh_mes: Decimal
    economia_mensal_reais: Decimal
