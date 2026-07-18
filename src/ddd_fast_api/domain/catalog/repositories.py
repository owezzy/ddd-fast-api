"""Catalog domain repository ports."""

from __future__ import annotations

from typing import Protocol

from ddd_fast_api.domain.catalog.entities import CatalogItem


class CatalogRepository(Protocol):
    """Port for retrieving catalog items."""

    def list_items(self) -> list[CatalogItem]:
        """Return the available catalog items."""
