"""Campos do motor de simulação (localização, resultado, projeções).

Revision ID: 20260524_001
Revises:
Create Date: 2026-05-24
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260524_001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("localizacoes", sa.Column("estado", sa.String(length=2), nullable=True))
    op.add_column(
        "localizacoes",
        sa.Column("hsp", sa.Numeric(precision=6, scale=2), nullable=True),
    )
    op.add_column(
        "localizacoes",
        sa.Column("tarifa_kwh", sa.Numeric(precision=8, scale=4), nullable=True),
    )
    op.add_column(
        "resultados",
        sa.Column("potencia_kwp", sa.Numeric(precision=8, scale=2), nullable=True),
    )
    op.add_column(
        "resultados", sa.Column("quantidade_paineis", sa.Integer(), nullable=True)
    )
    op.add_column(
        "resultados",
        sa.Column("area_minima_m2", sa.Numeric(precision=8, scale=2), nullable=True),
    )
    op.add_column("resultados", sa.Column("marcas_recomendadas", sa.Text(), nullable=True))
    op.add_column("resultados", sa.Column("observacao_gemini", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("resultados", "observacao_gemini")
    op.drop_column("resultados", "marcas_recomendadas")
    op.drop_column("resultados", "area_minima_m2")
    op.drop_column("resultados", "quantidade_paineis")
    op.drop_column("resultados", "potencia_kwp")
    op.drop_column("localizacoes", "tarifa_kwh")
    op.drop_column("localizacoes", "hsp")
    op.drop_column("localizacoes", "estado")
