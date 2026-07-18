"""Shared SQLAlchemy metadata for future ORM models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for future SQLAlchemy ORM models."""


metadata = Base.metadata
