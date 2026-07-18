"""Dependency providers for the sample catalog HTTP endpoints."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from ddd_fast_api.application.catalog import GetCatalogItem, ListCatalogItems
from ddd_fast_api.domain.catalog import CatalogRepository
from ddd_fast_api.entrypoints.http.catalog_memory import build_sample_catalog_repository
from ddd_fast_api.foundation import Settings, get_settings
from ddd_fast_api.infrastructure.persistence import SQLAlchemyCatalogRepository, create_engine


async def get_catalog_repository(
    settings: Annotated[Settings, Depends(get_settings)],
) -> AsyncIterator[CatalogRepository]:
    """Select the catalog repository implementation for the current request."""

    if settings.catalog_repository_backend == "memory":
        yield build_sample_catalog_repository()
        return

    engine = create_engine(settings)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with session_factory() as session:
        yield SQLAlchemyCatalogRepository(session)

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
