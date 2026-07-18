"""Tests for the sample identity HTTP endpoint."""

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from ddd_fast_api.bootstrap import app
from ddd_fast_api.foundation import Settings, get_settings
from ddd_fast_api.infrastructure.persistence import Base, create_engine
from ddd_fast_api.infrastructure.persistence.models import UserAccountModel


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


@pytest.mark.anyio
async def test_identity_route_can_select_sqlalchemy_adapter(tmp_path: Path) -> None:
    database_path = tmp_path / "identity.db"
    settings = Settings.model_validate(
        {
            "identity_repository_backend": "sqlalchemy",
            "database_url": f"sqlite+aiosqlite:///{database_path}",
        },
    )
    engine = create_engine(settings)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        session.add(
            UserAccountModel(
                id="user-db-1",
                email="db-user@example.com",
                display_name="Database user",
                status="active",
            ),
        )
        await session.commit()

    app.dependency_overrides[get_settings] = lambda: settings

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/identity/users/db-user@example.com")

    app.dependency_overrides.clear()
    await engine.dispose()

    assert response.status_code == 200
    assert response.json() == {
        "id": "user-db-1",
        "email": "db-user@example.com",
        "display_name": "Database user",
        "status": "active",
    }
