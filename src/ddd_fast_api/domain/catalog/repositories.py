"""Catalog domain repository ports."""

from __future__ import annotations

from typing import Protocol

from ddd_fast_api.domain.catalog.entities import CatalogItem
from ddd_fast_api.domain.catalog.value_objects import SKU


class CatalogRepository(Protocol):
    """Port for retrieving catalog items."""

    async def list_items(self) -> list[CatalogItem]:
        """Return the available catalog items."""

    async def get_item_by_sku(self, sku: SKU) -> CatalogItem | None:
        """Return one catalog item by SKU, if it exists."""
