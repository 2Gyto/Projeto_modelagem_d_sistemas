"""fluxo público: senha/telhado opcionais + quantidade_paineis

Revision ID: 002
Revises: 001
Create Date: 2026-05-28

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("usuarios", "senha_hash", existing_type=sa.String(255), nullable=True)
    op.alter_column("dados_telhado", "area_m2", existing_type=sa.Numeric(8, 2), nullable=True)
    op.alter_column(
        "dados_telhado",
        "orientacao",
        existing_type=sa.Enum(name="orientacao_telhado"),
        nullable=True,
    )
    op.alter_column(
        "dados_telhado",
        "tipo_conexao",
        existing_type=sa.Enum(name="tipo_conexao"),
        nullable=True,
    )
    op.add_column(
        "resultados",
        sa.Column("quantidade_paineis", sa.Integer(), nullable=True),
    )
    op.add_column(
        "resultados",
        sa.Column("potencia_sistema_kwp", sa.Numeric(8, 2), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("resultados", "potencia_sistema_kwp")
    op.drop_column("resultados", "quantidade_paineis")
    op.alter_column(
        "dados_telhado",
        "tipo_conexao",
        existing_type=sa.Enum(name="tipo_conexao"),
        nullable=False,
    )
    op.alter_column(
        "dados_telhado",
        "orientacao",
        existing_type=sa.Enum(name="orientacao_telhado"),
        nullable=False,
    )
    op.alter_column("dados_telhado", "area_m2", existing_type=sa.Numeric(8, 2), nullable=False)
    op.alter_column("usuarios", "senha_hash", existing_type=sa.String(255), nullable=False)
