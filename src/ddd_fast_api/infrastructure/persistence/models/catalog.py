"""SQLAlchemy ORM models for the catalog slice."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ddd_fast_api.infrastructure.persistence.base import Base


class CatalogItemModel(Base):
    """Persistence model for catalog items."""

    __tablename__ = "catalog_items"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="active")
