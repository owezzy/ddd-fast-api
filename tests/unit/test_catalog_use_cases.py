"""Tests for catalog application use cases."""

from dataclasses import dataclass

import pytest

from ddd_fast_api.application.catalog import GetCatalogItem, ListCatalogItems
from ddd_fast_api.domain.catalog import (
    SKU,
    CatalogFilters,
    CatalogItem,
    CatalogListQuery,
    CatalogRepository,
    CatalogSortField,
    CatalogUnitOfWork,
    PageParams,
    PaginatedCatalogItems,
    SortDirection,
)


@dataclass(slots=True)
class InMemoryCatalogRepository:
    items: list[CatalogItem]

    async def list_items(self, query: CatalogListQuery) -> PaginatedCatalogItems:
        return PaginatedCatalogItems(
            items=self.items,
            total_items=len(self.items),
            page=query.page.page,
            page_size=query.page.page_size,
        )

    async def get_item_by_sku(self, sku: SKU) -> CatalogItem | None:
        for item in self.items:
            if item.sku == sku:
                return item
        return None


@dataclass(slots=True)
class InMemoryCatalogUnitOfWork(CatalogUnitOfWork):
    _catalog_repository: CatalogRepository

    @property
    def catalog_repository(self) -> CatalogRepository:
        return self._catalog_repository

    async def __aenter__(self) -> "InMemoryCatalogUnitOfWork":
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None

    async def commit(self) -> None:
        return None

    async def rollback(self) -> None:
        return None


@pytest.mark.anyio
async def test_list_catalog_items_returns_repository_items() -> None:
    items = [
        CatalogItem(id="item-1", sku=SKU("SKU-001"), name="Starter item"),
        CatalogItem(id="item-2", sku=SKU("SKU-002"), name="Second item"),
    ]
    use_case = ListCatalogItems(
        unit_of_work_factory=lambda: InMemoryCatalogUnitOfWork(
            _catalog_repository=InMemoryCatalogRepository(items=items),
        ),
    )
    query = CatalogListQuery(
        filters=CatalogFilters(),
        sort_field=CatalogSortField.SKU,
        sort_direction=SortDirection.ASC,
        page=PageParams(page=1, page_size=20),
    )

    result = await use_case.execute(query)

    assert result.items == items
    assert result.total_items == 2


@pytest.mark.anyio
async def test_get_catalog_item_returns_matching_repository_item() -> None:
    items = [CatalogItem(id="item-1", sku=SKU("SKU-001"), name="Starter item")]
    use_case = GetCatalogItem(
        unit_of_work_factory=lambda: InMemoryCatalogUnitOfWork(
            _catalog_repository=InMemoryCatalogRepository(items=items),
        ),
    )

    result = await use_case.execute(SKU("sku-001"))

    assert result == items[0]


@pytest.mark.anyio
async def test_get_catalog_item_returns_none_when_missing() -> None:
    use_case = GetCatalogItem(
        unit_of_work_factory=lambda: InMemoryCatalogUnitOfWork(
            _catalog_repository=InMemoryCatalogRepository(items=[]),
        ),
    )

    result = await use_case.execute(SKU("SKU-404"))

    assert result is None
