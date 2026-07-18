"""Tests for the sample identity HTTP endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from ddd_fast_api.bootstrap import app


@pytest.mark.anyio
async def test_identity_route_returns_requested_account() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/identity/users/user@example.com")

    assert response.status_code == 200
    assert response.json() == {
        "id": "user-1",
        "email": "user@example.com",
        "display_name": "Starter user",
        "status": "active",
    }


@pytest.mark.anyio
async def test_identity_route_returns_not_found_error() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/identity/users/missing@example.com")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "user_account_not_found",
            "message": "User account not found.",
            "details": {"email": "missing@example.com"},
        }
    }


@pytest.mark.anyio
async def test_identity_route_rejects_invalid_email() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/identity/users/not-an-email")

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "invalid_user_email",
            "message": "Email address must contain '@'.",
            "details": {"email": "not-an-email"},
        }
    }
