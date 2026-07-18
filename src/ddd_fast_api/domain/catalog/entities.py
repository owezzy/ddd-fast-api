"""Catalog domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ddd_fast_api.domain.catalog.value_objects import SKU


class CatalogItemStatus(StrEnum):
    """Availability status for a catalog item."""

    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(slots=True)
class CatalogItem:
    """Catalog item entity with minimal lifecycle rules."""

    id: str
    sku: SKU
    name: str
    status: CatalogItemStatus = CatalogItemStatus.ACTIVE

    def __post_init__(self) -> None:
        normalized_name = self.name.strip()
        if not self.id.strip():
            raise ValueError("Catalog item id cannot be empty.")
        if len(normalized_name) < 3:
            raise ValueError("Catalog item name must contain at least 3 characters.")

        self.id = self.id.strip()
        self.name = normalized_name

    def deactivate(self) -> None:
        self.status = CatalogItemStatus.INACTIVE

    def activate(self) -> None:
        self.status = CatalogItemStatus.ACTIVE

    @property
    def is_active(self) -> bool:
        return self.status is CatalogItemStatus.ACTIVE
