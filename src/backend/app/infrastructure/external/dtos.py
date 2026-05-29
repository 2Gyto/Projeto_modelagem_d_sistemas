"""DTOs de resposta das APIs externas (camada infrastructure)."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CoordenadasCep:
    cep: str
    latitude: Decimal
    longitude: Decimal
    estado: str
    cidade: str


@dataclass(frozen=True)
class IndiceIrradiacao:
    hsp: Decimal
    fonte: str = "NASA POWER"


@dataclass(frozen=True)
class DadosMercadoGemini:
    tarifa_kwh: Decimal
    marcas_recomendadas: list[str]
    observacao: str | None = None
