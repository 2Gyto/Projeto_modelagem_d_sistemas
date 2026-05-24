import sqlite3
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from app.config import get_settings
from app.domain.exceptions import DomainError


@dataclass(frozen=True)
class TarifaUf:
    uf: str
    tarifa_kwh: Decimal
    taxa_disponibilidade_mono: Decimal
    taxa_disponibilidade_bi: Decimal
    taxa_disponibilidade_tri: Decimal
    atualizado_em: str
    fonte: str | None


class TarifaSqliteRepository:
    def __init__(self, db_path: str | None = None) -> None:
        self._path = Path(db_path or get_settings().tarifas_sqlite_path)

    def _connect(self) -> sqlite3.Connection:
        if not self._path.exists():
            raise DomainError(
                "Base de tarifas não encontrada. Execute scripts/seed_tarifas_uf.py."
            )
        return sqlite3.connect(self._path)

    def por_uf(self, uf: str) -> TarifaUf:
        sigla = uf.strip().upper()
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT uf, tarifa_kwh, taxa_disponibilidade_mono,
                       taxa_disponibilidade_bi, taxa_disponibilidade_tri,
                       atualizado_em, fonte
                FROM tarifas_uf WHERE uf = ?
                """,
                (sigla,),
            ).fetchone()
        if not row:
            raise DomainError(
                f"Tarifa indisponível para o estado {sigla}. (RB07)"
            )
        return TarifaUf(
            uf=row[0],
            tarifa_kwh=Decimal(str(row[1])),
            taxa_disponibilidade_mono=Decimal(str(row[2])),
            taxa_disponibilidade_bi=Decimal(str(row[3])),
            taxa_disponibilidade_tri=Decimal(str(row[4])),
            atualizado_em=row[5],
            fonte=row[6],
        )
