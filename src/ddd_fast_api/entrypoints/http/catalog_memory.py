"""Temporary in-memory adapter for the sample catalog endpoint."""

from __future__ import annotations

from dataclasses import dataclass, field

from ddd_fast_api.domain.catalog import (
    SKU,
    CatalogItem,
    CatalogItemStatus,
    CatalogListQuery,
    CatalogRepository,
    CatalogSortField,
    CatalogUnitOfWork,
    PaginatedCatalogItems,
    SortDirection,
)


@dataclass(slots=True)
class InMemoryCatalogRepository(CatalogRepository):
    """Edge-layer adapter supplying sample catalog data."""

    items: list[CatalogItem] = field(default_factory=list)

    async def list_items(self, query: CatalogListQuery) -> PaginatedCatalogItems:
        items = self.items

        if query.filters.status is not None:
            items = [item for item in items if item.status is query.filters.status]

        if query.filters.search is not None:
            search_term = query.filters.search.casefold()
            items = [
                item
                for item in items
                if search_term in item.name.casefold() or search_term in item.sku.value.casefold()
            ]

        reverse = query.sort_direction is SortDirection.DESC
        if query.sort_field is CatalogSortField.NAME:
            items = sorted(
                items,
                key=lambda item: (item.name.casefold(), item.sku.value),
                reverse=reverse,
            )
        else:
            items = sorted(items, key=lambda item: item.sku.value, reverse=reverse)

        total_items = len(items)
        start = query.page.offset
        end = start + query.page.page_size
        page_items = items[start:end]

        return PaginatedCatalogItems(
            items=page_items,
            total_items=total_items,
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
    """In-memory unit of work for catalog reads."""

    _catalog_repository: InMemoryCatalogRepository

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


def build_sample_catalog_repository() -> InMemoryCatalogRepository:
    """Create the temporary sample catalog dataset for the scaffold."""

    return InMemoryCatalogRepository(
        items=[
            CatalogItem(id="item-1", sku=SKU("SKU-001"), name="Starter item"),
            CatalogItem(id="item-2", sku=SKU("SKU-002"), name="Second item"),
            CatalogItem(
                id="item-3",
                sku=SKU("SKU-003"),
                name="Archived item",
                status=CatalogItemStatus.INACTIVE,
            ),
        ],
    )


def build_sample_catalog_unit_of_work() -> InMemoryCatalogUnitOfWork:
    """Create the in-memory catalog unit of work for sample queries."""

    return InMemoryCatalogUnitOfWork(_catalog_repository=build_sample_catalog_repository())
