"""Dependency providers for the sample catalog HTTP endpoints."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from ddd_fast_api.application.catalog import GetCatalogItem, ListCatalogItems
from ddd_fast_api.domain.catalog import CatalogRepository
from ddd_fast_api.entrypoints.http.catalog_memory import build_sample_catalog_repository
from ddd_fast_api.foundation import Settings, get_settings
from ddd_fast_api.infrastructure.persistence import (
    SQLAlchemyCatalogRepository,
    create_engine,
    create_session_factory_from_engine,
)


def _resolve_persistence_resources(
    request: Request,
    settings: Settings,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession], bool]:
    app_state = request.app.state
    state_settings = getattr(app_state, "settings", None)
    state_engine = getattr(app_state, "engine", None)
    state_session_factory = getattr(app_state, "session_factory", None)

    if (
        state_settings is not None
        and state_engine is not None
        and state_session_factory is not None
        and state_settings.database_url == settings.database_url
    ):
        return state_engine, state_session_factory, False

    engine = create_engine(settings)
    session_factory = create_session_factory_from_engine(engine)
    return engine, session_factory, True


async def get_catalog_repository(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> AsyncIterator[CatalogRepository]:
    """Select the catalog repository implementation for the current request."""

    if settings.catalog_repository_backend == "memory":
        yield build_sample_catalog_repository()
        return

    engine, session_factory, should_dispose_engine = _resolve_persistence_resources(
        request,
        settings,
    )

    async with session_factory() as session:
        yield SQLAlchemyCatalogRepository(session)

    if should_dispose_engine:
        await engine.dispose()


def get_list_catalog_items_use_case(
    repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
) -> ListCatalogItems:
    """Build the sample catalog list use case for the current scaffold."""

    return ListCatalogItems(repository=repository)


def get_catalog_item_use_case(
    repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
) -> GetCatalogItem:
    """Build the sample catalog detail use case for the current scaffold."""

    return GetCatalogItem(repository=repository)
