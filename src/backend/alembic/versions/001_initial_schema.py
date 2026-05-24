"""Schema inicial SolarCalc

Revision ID: 001
Revises:
Create Date: 2026-05-24
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("email", sa.String(150), nullable=False, unique=True),
        sa.Column("senha_hash", sa.String(255), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    status = postgresql.ENUM(
        "INICIADA",
        "VALIDANDO_DADOS",
        "BUSCANDO_IRRADIACAO",
        "CALCULANDO",
        "CONCLUIDA",
        "ERRO",
        name="status_simulacao",
        create_type=True,
    )
    tipo_entrada = postgresql.ENUM("KWH", "REAIS", name="tipo_entrada_consumo", create_type=True)
    orientacao = postgresql.ENUM(
        "NORTE", "SUL", "LESTE", "OESTE", name="orientacao_telhado", create_type=True
    )
    tipo_conexao = postgresql.ENUM(
        "MONOFASICA", "BIFASICA", "TRIFASICA", name="tipo_conexao", create_type=True
    )

    op.create_table(
        "simulacoes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "usuario_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("usuarios.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", status, nullable=False, server_default="INICIADA"),
        sa.Column(
            "realizada_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_table(
        "dados_consumo",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "simulacao_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("simulacoes.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column("consumo_kwh", sa.Numeric(10, 2)),
        sa.Column("valor_reais", sa.Numeric(10, 2)),
        sa.Column("tipo_entrada", tipo_entrada, nullable=False),
    )
    op.create_table(
        "localizacoes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "simulacao_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("simulacoes.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column("cep", sa.String(9)),
        sa.Column("cidade", sa.String(100)),
        sa.Column("uf", sa.String(2)),
        sa.Column("latitude", sa.Numeric(10, 8)),
        sa.Column("longitude", sa.Numeric(11, 8)),
        sa.Column("hsp_medio_dia", sa.Numeric(6, 3)),
        sa.Column("tarifa_kwh_usada", sa.Numeric(8, 4)),
    )
    op.create_table(
        "dados_telhado",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "simulacao_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("simulacoes.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column("area_m2", sa.Numeric(8, 2), nullable=False),
        sa.Column("orientacao", orientacao, nullable=False),
        sa.Column("tipo_conexao", tipo_conexao, nullable=False),
    )
    op.create_table(
        "resultados",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "simulacao_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("simulacoes.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column("geracao_kwh", sa.Numeric(10, 2)),
        sa.Column("potencia_kwp", sa.Numeric(8, 2)),
        sa.Column("qtd_paineis", sa.Integer),
        sa.Column("economia_mensal", sa.Numeric(10, 2)),
        sa.Column("payback_anos", sa.Numeric(6, 2)),
        sa.Column("payback_meses", sa.Numeric(6, 2)),
        sa.Column("custo_total", sa.Numeric(12, 2)),
        sa.Column("lucro_25_anos", sa.Numeric(14, 2)),
        sa.Column("ano_payback", sa.Integer),
    )
    op.create_table(
        "projecoes_anuais",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "resultado_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("resultados.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("ano", sa.Integer, nullable=False),
        sa.Column("custo_concessionaria", sa.Numeric(14, 2), nullable=False),
        sa.Column("custo_fotovoltaico", sa.Numeric(14, 2), nullable=False),
        sa.Column("saldo", sa.Numeric(14, 2), nullable=False),
    )
    op.create_table(
        "tarifas_concessionarias",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("concessionaria", sa.String(120), nullable=False),
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
        sa.Column("resolucao_aneel", sa.String(80)),
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
        op.execute(f"DROP TYPE IF EXISTS {name}")
