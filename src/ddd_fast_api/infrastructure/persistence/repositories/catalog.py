"""SQLAlchemy-backed repository for the catalog slice."""

from __future__ import annotations

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_fast_api.domain.catalog import (
    SKU,
    CatalogFilters,
    CatalogItem,
    CatalogListQuery,
    CatalogRepository,
    CatalogSortField,
    PaginatedCatalogItems,
    SortDirection,
)
from ddd_fast_api.infrastructure.persistence.mappers import to_domain_catalog_item
from ddd_fast_api.infrastructure.persistence.models import CatalogItemModel


class SQLAlchemyCatalogRepository(CatalogRepository):
    """Concrete catalog repository using SQLAlchemy async sessions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_items(self, query: CatalogListQuery) -> PaginatedCatalogItems:
        filtered_stmt = self._apply_model_filters(
            select(CatalogItemModel),
            query.filters,
        )

        count_stmt = self._apply_count_filters(
            select(func.count()).select_from(CatalogItemModel),
            query.filters,
        )
        count_result = await self.session.execute(count_stmt)
        total_items = count_result.scalar_one()

        stmt = self._apply_ordering(filtered_stmt, query)
        stmt = stmt.offset(query.page.offset).limit(query.page.page_size)

        result = await self.session.execute(stmt)
        items = [to_domain_catalog_item(model) for model in result.scalars().all()]

        return PaginatedCatalogItems(
            items=items,
            total_items=total_items,
            page=query.page.page,
            page_size=query.page.page_size,
        )

    async def get_item_by_sku(self, sku: SKU) -> CatalogItem | None:
        result = await self.session.execute(
            select(CatalogItemModel).where(CatalogItemModel.sku == sku.value),
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain_catalog_item(model)

    @staticmethod
    def _apply_model_filters(
        statement: Select[tuple[CatalogItemModel]],
        filters: CatalogFilters,
    ) -> Select[tuple[CatalogItemModel]]:
        if filters.status is not None:
            statement = statement.where(CatalogItemModel.status == filters.status.value)
        if filters.search is not None:
            statement = statement.where(CatalogItemModel.name.ilike(f"%{filters.search}%"))
        return statement

    @staticmethod
    def _apply_count_filters(
        statement: Select[tuple[int]],
        filters: CatalogFilters,
    ) -> Select[tuple[int]]:
        if filters.status is not None:
            statement = statement.where(CatalogItemModel.status == filters.status.value)
        if filters.search is not None:
            statement = statement.where(CatalogItemModel.name.ilike(f"%{filters.search}%"))
        return statement

    @staticmethod
    def _apply_ordering(
        statement: Select[tuple[CatalogItemModel]],
        query: CatalogListQuery,
    ) -> Select[tuple[CatalogItemModel]]:
        order_column = (
            CatalogItemModel.name
            if query.sort_field is CatalogSortField.NAME
            else CatalogItemModel.sku
        )
        if query.sort_direction is SortDirection.DESC:
            return statement.order_by(order_column.desc())
        return statement.order_by(order_column.asc())
