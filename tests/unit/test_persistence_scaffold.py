"""Tests for the persistence scaffold."""

from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from ddd_fast_api.foundation import Settings
from ddd_fast_api.infrastructure.persistence import create_engine, create_session_factory


def test_create_engine_uses_async_driver() -> None:
    settings = Settings(
        _env_file=None,
        database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/test_db",
    )

    engine = create_engine(settings)

    assert isinstance(engine, AsyncEngine)
    assert engine.url.drivername == "postgresql+asyncpg"


def test_create_session_factory_returns_async_sessionmaker() -> None:
    settings = Settings(
        _env_file=None,
        database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/test_db",
    )

    session_factory = create_session_factory(settings)

    assert isinstance(session_factory, async_sessionmaker)
    assert session_factory.class_ is AsyncSession


def test_alembic_entrypoints_exist() -> None:
    root = Path(__file__).resolve().parents[2]

    assert (root / "alembic.ini").exists()
    assert (root / "alembic" / "env.py").exists()
    assert (root / "alembic" / "script.py.mako").exists()
