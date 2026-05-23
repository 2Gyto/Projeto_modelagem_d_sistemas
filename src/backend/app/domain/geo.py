from dataclasses import dataclass


@dataclass(frozen=True)
class EnderecoGeo:
    cep: str
    uf: str
    cidade: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class DadosIrradiacao:
    """HSP em horas/dia; hsp_mensal = média diária de cada mês (YYYYMM)."""

    hsp_mensal: dict[str, float]
    hsp_medio: float
    ano_referencia: int
