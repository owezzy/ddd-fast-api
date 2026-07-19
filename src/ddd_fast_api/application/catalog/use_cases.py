"""Catalog application use cases."""

from __future__ import annotations

from dataclasses import dataclass

from ddd_fast_api.domain.catalog import (
    SKU,
    CatalogItem,
    CatalogListQuery,
    CatalogUnitOfWorkFactory,
    PaginatedCatalogItems,
)


@dataclass(slots=True)
class ListCatalogItems:
    """Read-only use case for catalog item retrieval."""

    unit_of_work_factory: CatalogUnitOfWorkFactory

    async def execute(self, query: CatalogListQuery) -> PaginatedCatalogItems:
        async with self.unit_of_work_factory() as unit_of_work:
            return await unit_of_work.catalog_repository.list_items(query)


@dataclass(slots=True)
class GetCatalogItem:
    """Read-only use case for retrieving a single catalog item by SKU."""

    unit_of_work_factory: CatalogUnitOfWorkFactory

    async def execute(self, sku: SKU) -> CatalogItem | None:
        async with self.unit_of_work_factory() as unit_of_work:
            return await unit_of_work.catalog_repository.get_item_by_sku(sku)
