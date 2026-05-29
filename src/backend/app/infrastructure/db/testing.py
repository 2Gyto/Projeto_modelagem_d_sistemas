"""Utilitários de banco para testes de integração (SQLite em memória ou arquivo temporário)."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import Enum as SAEnum
from sqlalchemy import Uuid, create_engine
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.db.base import Base

_sqlite_ready = False


def prepare_metadata_for_sqlite() -> None:
    """Adapta tipos PostgreSQL (UUID, ENUM nativo) para SQLite de teste."""
    global _sqlite_ready
    if _sqlite_ready:
        return
    for table in Base.metadata.tables.values():
        for col in table.columns:
            if isinstance(col.type, PGUUID):
                col.type = Uuid(as_uuid=True)
            elif isinstance(col.type, SAEnum):
                col.type.native_enum = False
    _sqlite_ready = True


def create_test_engine(
    database_url: str = "sqlite+pysqlite:///:memory:",
    *,
    echo: bool = False,
) -> Engine:
    prepare_metadata_for_sqlite()
    connect_args: dict[str, object] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(database_url, echo=echo, connect_args=connect_args)
    Base.metadata.create_all(engine)
    return engine


def create_test_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def drop_all_tables(engine: Engine) -> None:
    Base.metadata.drop_all(engine)


def session_scope(
    engine: Engine,
) -> Generator[Session, None, None]:
    factory = create_test_session_factory(engine)
    session = factory()
    try:
        yield session
    finally:
        session.close()


def reset_database(engine: Engine) -> None:
    drop_all_tables(engine)
    Base.metadata.create_all(engine)


def file_database_url(path: Path) -> str:
    return f"sqlite+pysqlite:///{path.as_posix()}"
