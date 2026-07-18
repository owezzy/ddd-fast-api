"""Tests for the initial executable scaffold."""

import pytest
from httpx import ASGITransport, AsyncClient

from ddd_fast_api.bootstrap import app


@pytest.mark.anyio
async def test_root_reports_foundation_scaffold() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "foundation-scaffold"


@pytest.mark.anyio
async def test_health_reports_ok() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
