"""SQLAlchemy ORM models for the identity slice."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ddd_fast_api.infrastructure.persistence.base import Base


class UserAccountModel(Base):
    """Persistence model for user accounts."""

    __tablename__ = "user_accounts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="active")
