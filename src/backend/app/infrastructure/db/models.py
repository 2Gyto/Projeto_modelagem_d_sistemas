import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import (
    OrientacaoTelhado,
    StatusSimulacao,
    TipoConexao,
    TipoEntradaConsumo,
)
from app.infrastructure.db.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    simulacoes: Mapped[list["Simulacao"]] = relationship(back_populates="usuario")


class Simulacao(Base):
    __tablename__ = "simulacoes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[StatusSimulacao] = mapped_column(
        Enum(StatusSimulacao, name="status_simulacao"),
        default=StatusSimulacao.INICIADA,
        nullable=False,
    )
    realizada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    usuario: Mapped["Usuario"] = relationship(back_populates="simulacoes")
    dados_consumo: Mapped["DadosConsumo | None"] = relationship(
        back_populates="simulacao", uselist=False
    )
    localizacao: Mapped["Localizacao | None"] = relationship(
        back_populates="simulacao", uselist=False
    )
    dados_telhado: Mapped["DadosTelhado | None"] = relationship(
        back_populates="simulacao", uselist=False
    )
    resultado: Mapped["Resultado | None"] = relationship(
        back_populates="simulacao", uselist=False
    )


class DadosConsumo(Base):
    __tablename__ = "dados_consumo"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    simulacao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("simulacoes.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    consumo_kwh: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    valor_reais: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    tipo_entrada: Mapped[TipoEntradaConsumo] = mapped_column(
        Enum(TipoEntradaConsumo, name="tipo_entrada_consumo"), nullable=False
    )

    simulacao: Mapped["Simulacao"] = relationship(back_populates="dados_consumo")


class Localizacao(Base):
    __tablename__ = "localizacoes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    simulacao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("simulacoes.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    cep: Mapped[str | None] = mapped_column(String(9))
    cidade: Mapped[str | None] = mapped_column(String(100))
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 8))
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(11, 8))

    simulacao: Mapped["Simulacao"] = relationship(back_populates="localizacao")


class DadosTelhado(Base):
    __tablename__ = "dados_telhado"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    simulacao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("simulacoes.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    area_m2: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    orientacao: Mapped[OrientacaoTelhado] = mapped_column(
        Enum(OrientacaoTelhado, name="orientacao_telhado"), nullable=False
    )
    tipo_conexao: Mapped[TipoConexao] = mapped_column(
        Enum(TipoConexao, name="tipo_conexao"), nullable=False
    )

    simulacao: Mapped["Simulacao"] = relationship(back_populates="dados_telhado")


class Resultado(Base):
    __tablename__ = "resultados"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    simulacao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("simulacoes.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    geracao_kwh: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    economia_mensal: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    payback_anos: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    payback_meses: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    custo_total: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    simulacao: Mapped["Simulacao"] = relationship(back_populates="resultado")
    projecoes: Mapped[list["ProjecaoAnual"]] = relationship(back_populates="resultado")


class ProjecaoAnual(Base):
    __tablename__ = "projecoes_anuais"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    resultado_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resultados.id", ondelete="CASCADE"),
        nullable=False,
    )
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    custo_concessionaria: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    custo_fotovoltaico: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    saldo: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)

    resultado: Mapped["Resultado"] = relationship(back_populates="projecoes")


class TarifaConcessionaria(Base):
    __tablename__ = "tarifas_concessionarias"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    concessionaria: Mapped[str] = mapped_column(String(120), nullable=False)
    tarifa_kwh: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    taxa_mono: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    taxa_bi: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    taxa_tri: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    resolucao_aneel: Mapped[str | None] = mapped_column(String(80))
