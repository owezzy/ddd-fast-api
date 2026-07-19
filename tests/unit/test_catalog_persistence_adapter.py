"""Tests for the SQLAlchemy-backed catalog repository adapter."""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from ddd_fast_api.domain.catalog import (
    SKU,
    CatalogFilters,
    CatalogItemStatus,
    CatalogListQuery,
    CatalogSortField,
    PageParams,
    SortDirection,
)
from ddd_fast_api.foundation import Settings
from ddd_fast_api.infrastructure.persistence import Base, SQLAlchemyCatalogRepository, create_engine
from ddd_fast_api.infrastructure.persistence.models import CatalogItemModel


@pytest.mark.anyio
async def test_sqlalchemy_catalog_repository_lists_items() -> None:
    settings = Settings(_env_file=None, database_url="sqlite+aiosqlite:///:memory:")
    engine = create_engine(settings)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        session.add_all(
            [
                CatalogItemModel(id="item-1", sku="SKU-001", name="Starter item", status="active"),
                CatalogItemModel(id="item-2", sku="SKU-002", name="Second item", status="inactive"),
            ],
        )
        await session.commit()

    async with session_factory() as session:
        repository = SQLAlchemyCatalogRepository(session)
        items = await repository.list_items(
            CatalogListQuery(
                filters=CatalogFilters(),
                sort_field=CatalogSortField.SKU,
                sort_direction=SortDirection.ASC,
                page=PageParams(page=1, page_size=20),
            ),
        )

    assert [item.sku.value for item in items.items] == ["SKU-001", "SKU-002"]
    assert items.items[1].status is CatalogItemStatus.INACTIVE
    assert items.total_items == 2

    await engine.dispose()


@pytest.mark.anyio
async def test_sqlalchemy_catalog_repository_gets_item_by_sku() -> None:
    settings = Settings(_env_file=None, database_url="sqlite+aiosqlite:///:memory:")
    engine = create_engine(settings)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        session.add(
            CatalogItemModel(
                id="item-1",
                sku="SKU-001",
                name="Starter item",
                status="active",
            ),
        )
        await session.commit()

    async with session_factory() as session:
        repository = SQLAlchemyCatalogRepository(session)
        item = await repository.get_item_by_sku(SKU("sku-001"))
        missing = await repository.get_item_by_sku(SKU("sku-404"))

    assert item is not None
    assert item.id == "item-1"
    assert item.name == "Starter item"
    assert missing is None

    await engine.dispose()


@pytest.mark.anyio
async def test_sqlalchemy_catalog_repository_applies_filters_and_pagination() -> None:
    settings = Settings.model_validate({"database_url": "sqlite+aiosqlite:///:memory:"})
    engine = create_engine(settings)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        session.add_all(
            [
                CatalogItemModel(id="item-1", sku="SKU-001", name="Starter item", status="active"),
                CatalogItemModel(id="item-2", sku="SKU-002", name="Second item", status="active"),
                CatalogItemModel(
                    id="item-3",
                    sku="SKU-003",
                    name="Archived item",
                    status="inactive",
                ),
            ],
        )
        await session.commit()

    async with session_factory() as session:
        repository = SQLAlchemyCatalogRepository(session)
        items = await repository.list_items(
            CatalogListQuery(
                filters=CatalogFilters(status=CatalogItemStatus.ACTIVE, search="item"),
                sort_field=CatalogSortField.NAME,
                sort_direction=SortDirection.DESC,
                page=PageParams(page=1, page_size=1),
            ),
        )

    assert [item.name for item in items.items] == ["Starter item"]
    assert items.total_items == 2
    assert items.total_pages == 2
    assert items.has_next is True

    await engine.dispose()
