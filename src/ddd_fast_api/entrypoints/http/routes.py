"""Minimal HTTP routes for the first executable scaffold."""

from fastapi import APIRouter, Depends

from ddd_fast_api.application.catalog import GetCatalogItem, ListCatalogItems
from ddd_fast_api.domain.catalog import SKU
from ddd_fast_api.entrypoints.http.catalog_dependencies import (
    get_catalog_item_use_case,
    get_list_catalog_items_use_case,
)
from ddd_fast_api.entrypoints.http.schemas import (
    CatalogItemResponse,
    CatalogItemsResponse,
    HealthResponse,
    RootResponse,
)
from ddd_fast_api.foundation import ProjectError

router = APIRouter()


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
async def list_catalog_items(
    use_case: ListCatalogItems = Depends(get_list_catalog_items_use_case),
) -> CatalogItemsResponse:
    """Return the sample catalog through the application-layer use case."""

    items = [CatalogItemResponse.from_domain(item) for item in await use_case.execute()]
    return CatalogItemsResponse(items=items)


@router.get("/catalog/items/{sku}", tags=["catalog"], response_model=CatalogItemResponse)
async def get_catalog_item(
    sku: str,
    use_case: GetCatalogItem = Depends(get_catalog_item_use_case),
) -> CatalogItemResponse:
    """Return one sample catalog item by SKU through the application layer."""

    try:
        catalog_sku = SKU(sku)
    except ValueError as exc:
        raise ProjectError(
            code="invalid_catalog_sku",
            message=str(exc),
            status_code=400,
            details={"sku": sku},
        ) from exc

    item = await use_case.execute(catalog_sku)
    if item is None:
        raise ProjectError(
            code="catalog_item_not_found",
            message="Catalog item not found.",
            status_code=404,
            details={"sku": catalog_sku.value},
        )

    return CatalogItemResponse.from_domain(item)
