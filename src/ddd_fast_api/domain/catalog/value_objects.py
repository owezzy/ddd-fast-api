"""Catalog domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class SKU:
    """Stock-keeping unit identifier for a catalog item."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()
        if not normalized:
            raise ValueError("SKU cannot be empty.")
        if len(normalized) < 3:
            raise ValueError("SKU must contain at least 3 characters.")
        if any(not (char.isalnum() or char == "-") for char in normalized):
            raise ValueError("SKU may contain only letters, numbers, and hyphens.")

        object.__setattr__(self, "value", normalized)


class CatalogItemStatus(StrEnum):
    """Availability status for a catalog item."""

    ACTIVE = "active"
    INACTIVE = "inactive"


class CatalogSortField(StrEnum):
    """Supported catalog ordering fields."""

    SKU = "sku"
    NAME = "name"


class SortDirection(StrEnum):
    """Supported sort directions for catalog lists."""

    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True, slots=True)
class CatalogFilters:
    """Filter criteria for listing catalog items."""

    status: CatalogItemStatus | None = None
    search: str | None = None

    def __post_init__(self) -> None:
        normalized_search = None
        if self.search is not None:
            normalized_search = self.search.strip()
            if not normalized_search:
                normalized_search = None
            elif len(normalized_search) < 2:
                raise ValueError("Catalog search must contain at least 2 characters.")

        object.__setattr__(self, "search", normalized_search)


@dataclass(frozen=True, slots=True)
class PageParams:
    """Pagination parameters for list queries."""

    page: int = 1
    page_size: int = 20

    def __post_init__(self) -> None:
        if self.page < 1:
            raise ValueError("Page number must be greater than or equal to 1.")
        if self.page_size < 1:
            raise ValueError("Page size must be greater than or equal to 1.")
        if self.page_size > 100:
            raise ValueError("Page size must be less than or equal to 100.")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


@dataclass(frozen=True, slots=True)
class CatalogListQuery:
    """List-query options for catalog retrieval."""

    filters: CatalogFilters = CatalogFilters()
    sort_field: CatalogSortField = CatalogSortField.SKU
    sort_direction: SortDirection = SortDirection.ASC
    page: PageParams = PageParams()
