import sqlite3
from decimal import Decimal
from pathlib import Path

from app.config import get_settings
from app.domain.exceptions import DomainError

_settings = get_settings()


def _caminho_sqlite() -> Path:
    if _settings.tarifas_sqlite_path:
        return Path(_settings.tarifas_sqlite_path)
    # src/backend/app/infrastructure/db -> parents[4] = src
    raiz_src = Path(__file__).resolve().parents[4]
    return raiz_src / "banco_de_dados" / "tarifas_por_uf.sqlite"


def _garantir_banco(db_path: Path) -> None:
    if db_path.is_file():
        return
    sql_path = db_path.parent / "tarifas_por_uf.sql"
    if not sql_path.is_file():
        raise DomainError(
            "Base de tarifas por UF não encontrada. Execute scripts/seed_tarifas_uf.py."
        )
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(sql_path.read_text(encoding="utf-8"))


class TarifaUfRepository:
    """Tarifa média de energia (R$/kWh) por UF — SQLite local."""

    def buscar_por_uf(self, uf: str) -> Decimal:
        sigla = uf.strip().upper()
        if len(sigla) != 2:
            raise DomainError("UF inválida.")

        db_path = _caminho_sqlite()
        _garantir_banco(db_path)

        with sqlite3.connect(db_path) as conn:
            row = conn.execute(
                "SELECT tarifa_kwh FROM tarifas_uf WHERE uf = ?",
                (sigla,),
            ).fetchone()

        if not row:
            raise DomainError(f"Tarifa não cadastrada para o estado {sigla}.")

        return Decimal(str(row[0]))
