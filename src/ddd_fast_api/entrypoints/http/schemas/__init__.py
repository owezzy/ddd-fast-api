"""HTTP boundary schemas for the scaffold entrypoints."""

from ddd_fast_api.entrypoints.http.schemas.catalog import (
    CatalogItemResponse,
    CatalogItemsQuery,
    CatalogItemsResponse,
)
from ddd_fast_api.entrypoints.http.schemas.identity import UserAccountResponse
from ddd_fast_api.entrypoints.http.schemas.meta import HealthResponse, RootResponse
from ddd_fast_api.entrypoints.http.schemas.runtime import (
    DevTokenRequest,
    HealthStatusResponse,
    PrincipalResponse,
    TokenResponse,
)

__all__ = [
    "CatalogItemResponse",
    "CatalogItemsQuery",
    "CatalogItemsResponse",
    "HealthResponse",
    "RootResponse",
    "UserAccountResponse",
    "DevTokenRequest",
    "HealthStatusResponse",
    "PrincipalResponse",
    "TokenResponse",
]
