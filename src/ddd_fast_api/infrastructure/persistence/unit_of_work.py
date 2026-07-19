"""Unit-of-work implementations for persistence-backed use cases."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from ddd_fast_api.domain.catalog import CatalogRepository, CatalogUnitOfWork
from ddd_fast_api.infrastructure.persistence.repositories.catalog import SQLAlchemyCatalogRepository


class SQLAlchemyCatalogUnitOfWork(CatalogUnitOfWork):
    """SQLAlchemy-backed catalog unit of work."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        engine: AsyncEngine,
        should_dispose_engine: bool,
    ) -> None:
        self._session_factory = session_factory
        self._engine = engine
        self._should_dispose_engine = should_dispose_engine
        self._session: AsyncSession | None = None
        self._catalog_repository: SQLAlchemyCatalogRepository | None = None

    @property
    def catalog_repository(self) -> CatalogRepository:
        assert self._catalog_repository is not None
        return self._catalog_repository

    async def __aenter__(self) -> "SQLAlchemyCatalogUnitOfWork":
        self._session = self._session_factory()
        self._catalog_repository = SQLAlchemyCatalogRepository(self._session)
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        assert self._session is not None
        if exc is not None:
            await self._session.rollback()
        await self._session.close()
        if self._should_dispose_engine:
            await self._engine.dispose()

    async def commit(self) -> None:
        if self._session is not None:
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session is not None:
            await self._session.rollback()
