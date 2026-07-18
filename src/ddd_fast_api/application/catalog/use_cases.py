"""Catalog application use cases."""

from __future__ import annotations

from dataclasses import dataclass

from ddd_fast_api.domain.catalog import SKU, CatalogItem, CatalogRepository


@dataclass(slots=True)
class ListCatalogItems:
    """Read-only use case for catalog item retrieval."""

    repository: CatalogRepository

    def execute(self) -> list[CatalogItem]:
        return self.repository.list_items()


@dataclass(slots=True)
class GetCatalogItem:
    """Read-only use case for retrieving a single catalog item by SKU."""

    repository: CatalogRepository

    def execute(self, sku: SKU) -> CatalogItem | None:
        return self.repository.get_item_by_sku(sku)
