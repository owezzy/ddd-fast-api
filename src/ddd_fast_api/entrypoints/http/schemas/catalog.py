"""Transport schemas for catalog endpoints."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ddd_fast_api.domain.catalog import (
    CatalogFilters,
    CatalogItem,
    CatalogItemStatus,
    CatalogListQuery,
    CatalogSortField,
    PageParams,
    PaginatedCatalogItems,
    SortDirection,
)


class CatalogItemResponse(BaseModel):
    """Boundary model for catalog items returned by the API."""

    id: str
    sku: str
    name: str
    status: CatalogItemStatus

    @classmethod
    def from_domain(cls, item: CatalogItem) -> "CatalogItemResponse":
        return cls(id=item.id, sku=item.sku.value, name=item.name, status=item.status)


class CatalogItemsResponse(BaseModel):
    """Boundary model for a list of catalog items."""

    items: list[CatalogItemResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def from_domain(cls, result: PaginatedCatalogItems) -> "CatalogItemsResponse":
        return cls(
            items=[CatalogItemResponse.from_domain(item) for item in result.items],
            page=result.page,
            page_size=result.page_size,
            total_items=result.total_items,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_previous=result.has_previous,
        )


class CatalogItemsQuery(BaseModel):
    """Boundary model for catalog list query parameters."""

    model_config = ConfigDict(extra="forbid")

    status: CatalogItemStatus | None = None
    search: str | None = Field(default=None, min_length=2, max_length=100)
    sort_by: Literal["sku", "name"] = "sku"
    sort_direction: Literal["asc", "desc"] = "asc"
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    def to_domain(self) -> CatalogListQuery:
        return CatalogListQuery(
            filters=CatalogFilters(status=self.status, search=self.search),
            sort_field=CatalogSortField(self.sort_by),
            sort_direction=SortDirection(self.sort_direction),
            page=PageParams(page=self.page, page_size=self.page_size),
        )
