"""Catalog application use cases."""

from __future__ import annotations

from dataclasses import dataclass

from ddd_fast_api.domain.catalog import CatalogItem, CatalogRepository


@dataclass(slots=True)
class ListCatalogItems:
    """Read-only use case for catalog item retrieval."""

    repository: CatalogRepository

    def execute(self) -> list[CatalogItem]:
        return self.repository.list_items()
