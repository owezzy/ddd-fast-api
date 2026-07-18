"""Tests for the initial catalog domain skeleton."""

import pytest

from ddd_fast_api.domain.catalog import SKU, CatalogItem, CatalogItemStatus


def test_sku_normalizes_to_uppercase() -> None:
    sku = SKU(" abc-123 ")

    assert sku.value == "ABC-123"


@pytest.mark.parametrize(
    ("raw_value", "message"),
    [
        ("", "SKU cannot be empty."),
        ("a1", "SKU must contain at least 3 characters."),
        ("ab$", "SKU may contain only letters, numbers, and hyphens."),
    ],
)
def test_sku_rejects_invalid_values(raw_value: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        SKU(raw_value)


def test_catalog_item_requires_meaningful_name() -> None:
    with pytest.raises(ValueError, match="Catalog item name must contain at least 3 characters."):
        CatalogItem(id="item-1", sku=SKU("SKU-001"), name=" a ")


def test_catalog_item_lifecycle_toggles_status() -> None:
    item = CatalogItem(id="item-1", sku=SKU("SKU-001"), name="Starter item")

    assert item.is_active is True
    assert item.status is CatalogItemStatus.ACTIVE

    item.deactivate()

    assert item.is_active is False
    assert item.status is CatalogItemStatus.INACTIVE

    item.activate()

    assert item.is_active is True
    assert item.status is CatalogItemStatus.ACTIVE
