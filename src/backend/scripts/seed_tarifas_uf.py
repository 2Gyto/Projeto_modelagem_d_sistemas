"""Cria/atualiza o SQLite de tarifas por UF. Execute: python scripts/seed_tarifas_uf.py"""

import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "tarifas_uf.db"

# Tarifas médias de referência (R$/kWh) e mínimo faturado (kWh) por tipo — valores ilustrativos ANEEL
TARIFAS_UF = [
    ("AC", 0.890, 30, 50, 100),
    ("AL", 0.860, 30, 50, 100),
    ("AP", 0.810, 30, 50, 100),
    ("AM", 0.940, 30, 50, 100),
    ("BA", 0.850, 30, 50, 100),
    ("CE", 0.870, 30, 50, 100),
    ("DF", 0.750, 30, 50, 100),
    ("ES", 0.780, 30, 50, 100),
    ("GO", 0.840, 30, 50, 100),
    ("MA", 0.920, 30, 50, 100),
    ("MT", 0.960, 30, 50, 100),
    ("MS", 0.890, 30, 50, 100),
    ("MG", 0.910, 30, 50, 100),
    ("PA", 1.050, 30, 50, 100),
    ("PB", 0.820, 30, 50, 100),
    ("PR", 0.790, 30, 50, 100),
    ("PE", 0.840, 30, 50, 100),
    ("PI", 0.930, 30, 50, 100),
    ("RJ", 0.980, 30, 50, 100),
    ("RN", 0.830, 30, 50, 100),
    ("RS", 0.810, 30, 50, 100),
    ("RO", 0.860, 30, 50, 100),
    ("RR", 0.880, 30, 50, 100),
    ("SC", 0.770, 30, 50, 100),
    ("SP", 0.830, 30, 50, 100),
    ("SE", 0.800, 30, 50, 100),
    ("TO", 0.870, 30, 50, 100),
]


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tarifas_uf (
            uf TEXT PRIMARY KEY,
            tarifa_kwh REAL NOT NULL,
            taxa_disponibilidade_mono REAL NOT NULL,
            taxa_disponibilidade_bi REAL NOT NULL,
            taxa_disponibilidade_tri REAL NOT NULL,
            atualizado_em TEXT NOT NULL,
            fonte TEXT
        )
        """
    )
    hoje = date.today().isoformat()
    for uf, tarifa, mono, bi, tri in TARIFAS_UF:
        conn.execute(
            """
            INSERT INTO tarifas_uf (
                uf, tarifa_kwh, taxa_disponibilidade_mono,
                taxa_disponibilidade_bi, taxa_disponibilidade_tri,
                atualizado_em, fonte
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(uf) DO UPDATE SET
                tarifa_kwh = excluded.tarifa_kwh,
                taxa_disponibilidade_mono = excluded.taxa_disponibilidade_mono,
                taxa_disponibilidade_bi = excluded.taxa_disponibilidade_bi,
                taxa_disponibilidade_tri = excluded.taxa_disponibilidade_tri,
                atualizado_em = excluded.atualizado_em,
                fonte = excluded.fonte
            """,
            (uf, tarifa, mono, bi, tri, hoje, "Referência média ANEEL — seed SolarCalc"),
        )
    conn.commit()
    conn.close()
    print(f"Tarifas gravadas em {DB_PATH} ({len(TARIFAS_UF)} UFs)")


if __name__ == "__main__":
    main()
