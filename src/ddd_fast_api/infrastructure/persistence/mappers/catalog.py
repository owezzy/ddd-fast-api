"""Mapping helpers for catalog persistence models."""

from ddd_fast_api.domain.catalog import SKU, CatalogItem, CatalogItemStatus
from ddd_fast_api.infrastructure.persistence.models import CatalogItemModel


def to_domain_catalog_item(model: CatalogItemModel) -> CatalogItem:
    """Translate an ORM model into the catalog domain entity."""

    return CatalogItem(
        id=model.id,
        sku=SKU(model.sku),
        name=model.name,
        status=CatalogItemStatus(model.status),
    )
