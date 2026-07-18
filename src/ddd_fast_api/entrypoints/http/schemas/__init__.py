"""HTTP boundary schemas for the scaffold entrypoints."""

from ddd_fast_api.entrypoints.http.schemas.catalog import CatalogItemResponse, CatalogItemsResponse
from ddd_fast_api.entrypoints.http.schemas.identity import UserAccountResponse
from ddd_fast_api.entrypoints.http.schemas.meta import HealthResponse, RootResponse

__all__ = [
    "CatalogItemResponse",
    "CatalogItemsResponse",
    "HealthResponse",
    "RootResponse",
    "UserAccountResponse",
]
