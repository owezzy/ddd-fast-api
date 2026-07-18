"""Async SQLAlchemy engine and session scaffolding."""

from __future__ import annotations

from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ddd_fast_api.foundation import Settings, get_settings


def create_engine(settings: Settings) -> AsyncEngine:
    """Build the project async engine from settings."""

    return create_async_engine(
        settings.database_url,
        echo=settings.app_debug,
        pool_pre_ping=True,
    )


def create_session_factory(settings: Settings) -> async_sessionmaker[AsyncSession]:
    """Build the async session factory for the project."""

    return async_sessionmaker(bind=create_engine(settings), expire_on_commit=False)


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """Return the shared async engine for the current process."""

    return create_engine(get_settings())


@lru_cache(maxsize=1)
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return the shared async session factory for the current process."""

    return create_session_factory(get_settings())
