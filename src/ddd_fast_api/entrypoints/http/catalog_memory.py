"""Temporary in-memory adapter for the sample catalog endpoint."""

from __future__ import annotations

from dataclasses import dataclass, field

from ddd_fast_api.domain.catalog import SKU, CatalogItem, CatalogRepository


@dataclass(slots=True)
class InMemoryCatalogRepository(CatalogRepository):
    """Edge-layer adapter supplying sample catalog data."""

    items: list[CatalogItem] = field(default_factory=list)

    def list_items(self) -> list[CatalogItem]:
        return self.items


def build_sample_catalog_repository() -> InMemoryCatalogRepository:
    """Create the temporary sample catalog dataset for the scaffold."""

    return InMemoryCatalogRepository(
        items=[
            CatalogItem(id="item-1", sku=SKU("SKU-001"), name="Starter item"),
            CatalogItem(id="item-2", sku=SKU("SKU-002"), name="Second item"),
        ],
    )
