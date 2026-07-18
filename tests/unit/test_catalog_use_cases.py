"""Tests for catalog application use cases."""

from dataclasses import dataclass

from ddd_fast_api.application.catalog import ListCatalogItems
from ddd_fast_api.domain.catalog import SKU, CatalogItem


@dataclass(slots=True)
class InMemoryCatalogRepository:
    items: list[CatalogItem]

    def list_items(self) -> list[CatalogItem]:
        return self.items


def test_list_catalog_items_returns_repository_items() -> None:
    items = [
        CatalogItem(id="item-1", sku=SKU("SKU-001"), name="Starter item"),
        CatalogItem(id="item-2", sku=SKU("SKU-002"), name="Second item"),
    ]
    use_case = ListCatalogItems(repository=InMemoryCatalogRepository(items=items))

    result = use_case.execute()

    assert result == items
