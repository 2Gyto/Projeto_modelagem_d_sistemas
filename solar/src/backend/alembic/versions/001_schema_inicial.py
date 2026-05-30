"""schema inicial SolarCalc (ADR-06)

Revision ID: 001
Revises:
Create Date: 2026-05-21

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    status_sim = sa.Enum(
        "INICIADA",
        "VALIDANDO_DADOS",
        "BUSCANDO_IRRADIACAO",
        "CALCULANDO",
        "CONCLUIDA",
        "ERRO",
        name="status_simulacao",
    )
    tipo_entrada = sa.Enum("KWH", "REAIS", name="tipo_entrada_consumo")
    orientacao = sa.Enum("NORTE", "SUL", "LESTE", "OESTE", name="orientacao_telhado")
    tipo_conexao = sa.Enum(
        "MONOFASICA", "BIFASICA", "TRIFASICA", name="tipo_conexao"
    )

    op.create_table(
        "simulacoes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("usuario_id", sa.UUID(), nullable=False),
        sa.Column("status", status_sim, nullable=False),
        sa.Column(
            "realizada_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "dados_consumo",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("simulacao_id", sa.UUID(), nullable=False),
        sa.Column("consumo_kwh", sa.Numeric(10, 2), nullable=True),
        sa.Column("valor_reais", sa.Numeric(10, 2), nullable=True),
        sa.Column("tipo_entrada", tipo_entrada, nullable=False),
        sa.ForeignKeyConstraint(
            ["simulacao_id"], ["simulacoes.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("simulacao_id"),
    )

    op.create_table(
        "localizacoes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("simulacao_id", sa.UUID(), nullable=False),
        sa.Column("cep", sa.String(length=9), nullable=True),
        sa.Column("cidade", sa.String(length=100), nullable=True),
        sa.Column("latitude", sa.Numeric(10, 8), nullable=True),
        sa.Column("longitude", sa.Numeric(11, 8), nullable=True),
        sa.ForeignKeyConstraint(
            ["simulacao_id"], ["simulacoes.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("simulacao_id"),
    )

    op.create_table(
        "dados_telhado",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("simulacao_id", sa.UUID(), nullable=False),
        sa.Column("area_m2", sa.Numeric(8, 2), nullable=False),
        sa.Column("orientacao", orientacao, nullable=False),
        sa.Column("tipo_conexao", tipo_conexao, nullable=False),
        sa.ForeignKeyConstraint(
            ["simulacao_id"], ["simulacoes.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("simulacao_id"),
    )

    op.create_table(
        "resultados",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("simulacao_id", sa.UUID(), nullable=False),
        sa.Column("geracao_kwh", sa.Numeric(10, 2), nullable=True),
        sa.Column("economia_mensal", sa.Numeric(10, 2), nullable=True),
        sa.Column("payback_anos", sa.Numeric(6, 2), nullable=True),
        sa.Column("payback_meses", sa.Numeric(6, 2), nullable=True),
        sa.Column("custo_total", sa.Numeric(12, 2), nullable=True),
        sa.ForeignKeyConstraint(
            ["simulacao_id"], ["simulacoes.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("simulacao_id"),
    )

    op.create_table(
        "projecoes_anuais",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("resultado_id", sa.UUID(), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("custo_concessionaria", sa.Numeric(14, 2), nullable=False),
        sa.Column("custo_fotovoltaico", sa.Numeric(14, 2), nullable=False),
        sa.Column("saldo", sa.Numeric(14, 2), nullable=False),
        sa.ForeignKeyConstraint(
            ["resultado_id"], ["resultados.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tarifas_concessionarias",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("concessionaria", sa.String(length=120), nullable=False),
        sa.Column("tarifa_kwh", sa.Numeric(8, 4), nullable=False),
        sa.Column("taxa_mono", sa.Numeric(8, 2), nullable=False),
        sa.Column("taxa_bi", sa.Numeric(8, 2), nullable=False),
        sa.Column("taxa_tri", sa.Numeric(8, 2), nullable=False),
        sa.Column(
            "atualizado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("resolucao_aneel", sa.String(length=80), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tarifas_concessionarias")
    op.drop_table("projecoes_anuais")
    op.drop_table("resultados")
    op.drop_table("dados_telhado")
    op.drop_table("localizacoes")
    op.drop_table("dados_consumo")
    op.drop_table("simulacoes")
    op.drop_table("usuarios")
    for name in (
        "tipo_conexao",
        "orientacao_telhado",
        "tipo_entrada_consumo",
        "status_simulacao",
    ):
        sa.Enum(name=name).drop(op.get_bind(), checkfirst=True)
