"""Integration test for the catalog SQLAlchemy-backed HTTP path."""

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from ddd_fast_api.bootstrap import create_app
from ddd_fast_api.foundation import Settings, get_settings
from ddd_fast_api.infrastructure.persistence import Base
from ddd_fast_api.infrastructure.persistence.models import CatalogItemModel


@pytest.mark.anyio
async def test_catalog_items_route_works_with_sqlalchemy_backend(tmp_path: Path) -> None:
    database_path = tmp_path / "integration-catalog.db"
    settings = Settings.model_validate(
        {
            "catalog_repository_backend": "sqlalchemy",
            "database_url": f"sqlite+aiosqlite:///{database_path}",
            "app_env": "test",
        },
    )
    app = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings

    async with app.router.lifespan_context(app):
        engine = app.state.engine
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        async with session_factory() as session:
            session.add(
                CatalogItemModel(
                    id="item-int-1",
                    sku="SKU-INT1",
                    name="Integration item",
                    status="active",
                ),
            )
            await session.commit()

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
        ) as client:
            response = await client.get("/catalog/items")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "item-int-1",
                "sku": "SKU-INT1",
                "name": "Integration item",
                "status": "active",
            },
        ],
        "page": 1,
        "page_size": 20,
        "total_items": 1,
        "total_pages": 1,
        "has_next": False,
        "has_previous": False,
    }
