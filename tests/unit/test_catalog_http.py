"""Tests for the sample catalog HTTP endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from ddd_fast_api.bootstrap import app


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
        ]
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
