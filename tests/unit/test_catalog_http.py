"""Tests for the sample catalog HTTP endpoint."""

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from ddd_fast_api.bootstrap import app
from ddd_fast_api.foundation import Settings, get_settings
from ddd_fast_api.infrastructure.persistence import Base, create_engine
from ddd_fast_api.infrastructure.persistence.models import CatalogItemModel


@pytest.mark.anyio
async def test_catalog_items_route_uses_application_layer_shape() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/catalog/items")

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "item-1",
                "sku": "SKU-001",
                "name": "Starter item",
                "status": "active",
            },
            {
                "id": "item-2",
                "sku": "SKU-002",
                "name": "Second item",
                "status": "active",
            },
            {
                "id": "item-3",
                "sku": "SKU-003",
                "name": "Archived item",
                "status": "inactive",
            },
        ],
        "page": 1,
        "page_size": 20,
        "total_items": 3,
        "total_pages": 1,
        "has_next": False,
        "has_previous": False,
    }


@pytest.mark.anyio
async def test_catalog_item_detail_route_returns_requested_item() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/catalog/items/SKU-001")

    assert response.status_code == 200
    assert response.json() == {
        "id": "item-1",
        "sku": "SKU-001",
        "name": "Starter item",
        "status": "active",
    }


@pytest.mark.anyio
async def test_catalog_item_detail_route_returns_not_found_error() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/catalog/items/SKU-999")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "catalog_item_not_found",
            "message": "Catalog item not found.",
            "details": {"sku": "SKU-999"},
        }
    }


@pytest.mark.anyio
async def test_catalog_item_detail_route_rejects_invalid_sku() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/catalog/items/%20")

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "invalid_catalog_sku",
            "message": "SKU cannot be empty.",
            "details": {"sku": " "},
        }
    }


@pytest.mark.anyio
async def test_catalog_routes_can_select_sqlalchemy_adapter(tmp_path: Path) -> None:
    database_path = tmp_path / "catalog.db"
    settings = Settings.model_validate(
        {
            "catalog_repository_backend": "sqlalchemy",
            "database_url": f"sqlite+aiosqlite:///{database_path}",
        },
    )
    engine = create_engine(settings)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        session.add(
            CatalogItemModel(
                id="item-db-1",
                sku="SKU-DB1",
                name="Database item",
                status="active",
            ),
        )
        await session.commit()

    app.dependency_overrides[get_settings] = lambda: settings

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        list_response = await client.get("/catalog/items")
        detail_response = await client.get("/catalog/items/SKU-DB1")

    app.dependency_overrides.clear()
    await engine.dispose()

    assert list_response.status_code == 200
    assert list_response.json() == {
        "items": [
            {
                "id": "item-db-1",
                "sku": "SKU-DB1",
                "name": "Database item",
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
    assert detail_response.status_code == 200
    assert detail_response.json() == {
        "id": "item-db-1",
        "sku": "SKU-DB1",
        "name": "Database item",
        "status": "active",
    }


@pytest.mark.anyio
async def test_catalog_items_route_supports_filter_order_and_pagination() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(
            "/catalog/items",
            params={
                "status": "active",
                "search": "item",
                "sort_by": "name",
                "sort_direction": "desc",
                "page": 1,
                "page_size": 1,
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": "item-1",
                "sku": "SKU-001",
                "name": "Starter item",
                "status": "active",
            },
        ],
        "page": 1,
        "page_size": 1,
        "total_items": 2,
        "total_pages": 2,
        "has_next": True,
        "has_previous": False,
    }
