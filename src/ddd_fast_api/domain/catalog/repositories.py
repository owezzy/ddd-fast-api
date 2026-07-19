"""Catalog domain repository ports."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, Self

from ddd_fast_api.domain.catalog.entities import CatalogItem
from ddd_fast_api.domain.catalog.value_objects import SKU, CatalogListQuery


@dataclass(frozen=True, slots=True)
class PaginatedCatalogItems:
    """Paginated catalog items returned from repository queries."""

    items: list[CatalogItem]
    total_items: int
    page: int
    page_size: int

    def __post_init__(self) -> None:
        if self.total_items < 0:
            raise ValueError("Total items cannot be negative.")

    @property
    def total_pages(self) -> int:
        if self.total_items == 0:
            return 0
        return (self.total_items + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1


class CatalogRepository(Protocol):
    """Port for retrieving catalog items."""

    async def list_items(self, query: CatalogListQuery) -> PaginatedCatalogItems:
        """Return the available catalog items for a typed list query."""

    async def get_item_by_sku(self, sku: SKU) -> CatalogItem | None:
        """Return one catalog item by SKU, if it exists."""


class CatalogUnitOfWork(Protocol):
    """Explicit transaction boundary for catalog use cases."""

    @property
    def catalog_repository(self) -> CatalogRepository:
        """Return the repository scoped to this unit of work."""

    async def __aenter__(self) -> Self:
        """Enter the unit-of-work scope."""

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Exit the unit-of-work scope."""

    async def commit(self) -> None:
        """Commit the current unit of work."""

    async def rollback(self) -> None:
        """Rollback the current unit of work."""


CatalogUnitOfWorkFactory = Callable[[], CatalogUnitOfWork]
