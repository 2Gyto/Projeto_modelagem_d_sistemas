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
    """Entrada RF01–RF04."""

    consumo_kwh: Decimal | None = Field(default=None, gt=0)
    valor_reais: Decimal | None = Field(default=None, gt=0)
    tipo_entrada: str
    cep: str = Field(min_length=8, max_length=9)
    area_m2: Decimal = Field(gt=0)
    orientacao: str
    tipo_conexao: str


class SimulacaoCompletaCreate(SimulacaoCreate):
    """Cria e executa o pipeline em uma única requisição."""


class ProjecaoAnualResponse(BaseModel):
    ano: int
    custo_concessionaria: Decimal
    custo_fotovoltaico: Decimal


class LocalizacaoResponse(BaseModel):
    cep: str | None
    uf: str | None
    cidade: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    hsp_medio_dia: Decimal | None
    tarifa_kwh: Decimal | None


class ResultadoDetalheResponse(BaseModel):
    geracao_kwh_mes: Decimal | None
    potencia_kwp: Decimal | None
    qtd_paineis: int | None
    economia_mensal: Decimal | None
    investimento: Decimal | None
    payback_anos: int
    payback_meses: int
    payback_texto: str
    lucro_25_anos: Decimal | None
    ano_payback: int | None
    marcas: str
    consumo_kwh_mes: Decimal | None
    projecoes: list[ProjecaoAnualResponse]


class SimulacaoResponse(BaseModel):
    id: uuid.UUID
    status: StatusSimulacao
    realizada_em: datetime

    model_config = {"from_attributes": True}


class TelhadoResponse(BaseModel):
    area_m2: Decimal
    orientacao: str
    tipo_conexao: str


class SimulacaoDetalheResponse(BaseModel):
    id: uuid.UUID
    status: StatusSimulacao
    realizada_em: datetime
    localizacao: LocalizacaoResponse | None = None
    telhado: TelhadoResponse | None = None
    resultado: ResultadoDetalheResponse | None = None


class HealthResponse(BaseModel):
    status: str
    app: str
