"""Minimal HTTP routes for the first executable scaffold."""

from fastapi import APIRouter, Depends

from ddd_fast_api.application.catalog import ListCatalogItems
from ddd_fast_api.entrypoints.http.catalog_memory import build_sample_catalog_repository
from ddd_fast_api.entrypoints.http.schemas import (
    CatalogItemResponse,
    CatalogItemsResponse,
    HealthResponse,
    RootResponse,
)

router = APIRouter()


def get_list_catalog_items_use_case() -> ListCatalogItems:
    """Build the sample catalog list use case for the current scaffold."""

    return ListCatalogItems(repository=build_sample_catalog_repository())


@router.get("/", tags=["meta"], response_model=RootResponse)
def root() -> RootResponse:
    """Describe the current state of the project."""

    return RootResponse(
        name="ddd-fast-api",
        status="foundation-scaffold",
        message="The first executable foundation slice is in place.",
    )


@router.get("/health", tags=["meta"], response_model=HealthResponse)
def health() -> HealthResponse:
    """Simple health endpoint for local validation."""

    return HealthResponse(status="ok")


@router.get("/catalog/items", tags=["catalog"], response_model=CatalogItemsResponse)
def list_catalog_items(
    use_case: ListCatalogItems = Depends(get_list_catalog_items_use_case),
) -> CatalogItemsResponse:
    """Return the sample catalog through the application-layer use case."""

    items = [CatalogItemResponse.from_domain(item) for item in use_case.execute()]
    return CatalogItemsResponse(items=items)
