"""Persistence scaffolding for SQLAlchemy async and Alembic."""

from ddd_fast_api.infrastructure.persistence.base import Base, metadata
from ddd_fast_api.infrastructure.persistence.database import (
    create_engine,
    create_session_factory,
    create_session_factory_from_engine,
    get_engine,
    get_session_factory,
)
from ddd_fast_api.infrastructure.persistence.models import CatalogItemModel, UserAccountModel
from ddd_fast_api.infrastructure.persistence.repositories import (
    SQLAlchemyCatalogRepository,
    SQLAlchemyIdentityRepository,
)
from ddd_fast_api.infrastructure.persistence.unit_of_work import SQLAlchemyCatalogUnitOfWork

__all__ = [
    "Base",
    "CatalogItemModel",
    "SQLAlchemyCatalogUnitOfWork",
    "SQLAlchemyCatalogRepository",
    "SQLAlchemyIdentityRepository",
    "UserAccountModel",
    "create_engine",
    "create_session_factory",
    "create_session_factory_from_engine",
    "get_engine",
    "get_session_factory",
    "metadata",
]
