"""Transport schemas for catalog endpoints."""

from pydantic import BaseModel

from ddd_fast_api.domain.catalog import CatalogItem, CatalogItemStatus


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
