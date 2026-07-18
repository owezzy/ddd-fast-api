"""SQLAlchemy-backed repository for the catalog slice."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_fast_api.domain.catalog import SKU, CatalogItem, CatalogRepository
from ddd_fast_api.infrastructure.persistence.mappers import to_domain_catalog_item
from ddd_fast_api.infrastructure.persistence.models import CatalogItemModel


class SQLAlchemyCatalogRepository(CatalogRepository):
    """Concrete catalog repository using SQLAlchemy async sessions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_items(self) -> list[CatalogItem]:
        result = await self.session.execute(
            select(CatalogItemModel).order_by(CatalogItemModel.sku),
        )
        return [to_domain_catalog_item(model) for model in result.scalars().all()]

    async def get_item_by_sku(self, sku: SKU) -> CatalogItem | None:
        result = await self.session.execute(
            select(CatalogItemModel).where(CatalogItemModel.sku == sku.value),
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain_catalog_item(model)
