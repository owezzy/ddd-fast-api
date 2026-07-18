"""Persistence scaffolding for SQLAlchemy async and Alembic."""

from ddd_fast_api.infrastructure.persistence.base import Base, metadata
from ddd_fast_api.infrastructure.persistence.database import (
    create_engine,
    create_session_factory,
    get_engine,
    get_session_factory,
)
from ddd_fast_api.infrastructure.persistence.models import CatalogItemModel
from ddd_fast_api.infrastructure.persistence.repositories import SQLAlchemyCatalogRepository

__all__ = [
    "Base",
    "CatalogItemModel",
    "SQLAlchemyCatalogRepository",
    "create_engine",
    "create_session_factory",
    "get_engine",
    "get_session_factory",
    "metadata",
]
