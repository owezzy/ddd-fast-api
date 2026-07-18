"""create catalog_items table

Revision ID: 20260718_183900
Revises: None
Create Date: 2026-07-18 18:39:00
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260718_183900"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "catalog_items",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("sku", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="active"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_catalog_items_sku"), "catalog_items", ["sku"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_catalog_items_sku"), table_name="catalog_items")
    op.drop_table("catalog_items")
