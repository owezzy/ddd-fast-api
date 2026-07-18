"""Tests for catalog application use cases."""

from dataclasses import dataclass

from ddd_fast_api.application.catalog import GetCatalogItem, ListCatalogItems
from ddd_fast_api.domain.catalog import SKU, CatalogItem


@dataclass(slots=True)
class InMemoryCatalogRepository:
    items: list[CatalogItem]

    def list_items(self) -> list[CatalogItem]:
        return self.items

    def get_item_by_sku(self, sku: SKU) -> CatalogItem | None:
        for item in self.items:
            if item.sku == sku:
                return item
        return None


def test_list_catalog_items_returns_repository_items() -> None:
    items = [
        CatalogItem(id="item-1", sku=SKU("SKU-001"), name="Starter item"),
        CatalogItem(id="item-2", sku=SKU("SKU-002"), name="Second item"),
    ]
    use_case = ListCatalogItems(repository=InMemoryCatalogRepository(items=items))

    result = use_case.execute()

    assert result == items


def test_get_catalog_item_returns_matching_repository_item() -> None:
    items = [CatalogItem(id="item-1", sku=SKU("SKU-001"), name="Starter item")]
    use_case = GetCatalogItem(repository=InMemoryCatalogRepository(items=items))

    result = use_case.execute(SKU("sku-001"))

    assert result == items[0]


def test_get_catalog_item_returns_none_when_missing() -> None:
    use_case = GetCatalogItem(repository=InMemoryCatalogRepository(items=[]))

    result = use_case.execute(SKU("SKU-404"))

    assert result is None
