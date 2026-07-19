"""Minimal HTTP routes for the first executable scaffold."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ddd_fast_api.application.catalog import GetCatalogItem, ListCatalogItems
from ddd_fast_api.application.identity import GetUserAccountByEmail
from ddd_fast_api.domain.catalog import SKU
from ddd_fast_api.domain.identity import EmailAddress
from ddd_fast_api.entrypoints.http.catalog_dependencies import (
    get_catalog_item_use_case,
    get_list_catalog_items_use_case,
)
from ddd_fast_api.entrypoints.http.identity_dependencies import (
    get_user_account_by_email_use_case,
)
from ddd_fast_api.entrypoints.http.schemas import (
    CatalogItemResponse,
    CatalogItemsQuery,
    CatalogItemsResponse,
    HealthResponse,
    RootResponse,
    UserAccountResponse,
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
    query: Annotated[CatalogItemsQuery, Query()] = CatalogItemsQuery(),
) -> CatalogItemsResponse:
    """Return the sample catalog through the application-layer use case."""

    result = await use_case.execute(query.to_domain())
    return CatalogItemsResponse.from_domain(result)


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


@router.get("/identity/users/{email}", tags=["identity"], response_model=UserAccountResponse)
async def get_user_account(
    email: str,
    use_case: GetUserAccountByEmail = Depends(get_user_account_by_email_use_case),
) -> UserAccountResponse:
    """Return one sample user account by email through the application layer."""

    try:
        user_email = EmailAddress(email)
    except ValueError as exc:
        raise ProjectError(
            code="invalid_user_email",
            message=str(exc),
            status_code=400,
            details={"email": email},
        ) from exc

    account = await use_case.execute(user_email)
    if account is None:
        raise ProjectError(
            code="user_account_not_found",
            message="User account not found.",
            status_code=404,
            details={"email": user_email.value},
        )

    return UserAccountResponse.from_domain(account)
