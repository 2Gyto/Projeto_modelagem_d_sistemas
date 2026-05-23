"""
Cria/atualiza src/banco_de_dados/tarifas_por_uf.sqlite a partir de tarifas_por_uf.sql.

Uso (na pasta src/backend):
    python scripts/seed_tarifas_uf.py
"""

from pathlib import Path
import sqlite3

RAIZ_SRC = Path(__file__).resolve().parents[2]
SQL_FILE = RAIZ_SRC / "banco_de_dados" / "tarifas_por_uf.sql"
DB_FILE = RAIZ_SRC / "banco_de_dados" / "tarifas_por_uf.sqlite"


def main() -> None:
    if not SQL_FILE.is_file():
        raise SystemExit(f"Arquivo SQL não encontrado: {SQL_FILE}")

    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    script = SQL_FILE.read_text(encoding="utf-8")

    with sqlite3.connect(DB_FILE) as conn:
        conn.executescript(script)
        count = conn.execute("SELECT COUNT(*) FROM tarifas_uf").fetchone()[0]

    print(f"OK: {DB_FILE} ({count} UFs)")


if __name__ == "__main__":
    main()
