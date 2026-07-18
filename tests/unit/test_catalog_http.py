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
