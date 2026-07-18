"""Integration test for the identity SQLAlchemy-backed HTTP path."""

from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from ddd_fast_api.bootstrap import create_app
from ddd_fast_api.foundation import Settings, get_settings
from ddd_fast_api.infrastructure.persistence import Base
from ddd_fast_api.infrastructure.persistence.models import UserAccountModel


@pytest.mark.anyio
async def test_identity_route_works_with_sqlalchemy_backend(tmp_path: Path) -> None:
    database_path = tmp_path / "integration-identity.db"
    settings = Settings.model_validate(
        {
            "identity_repository_backend": "sqlalchemy",
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
                UserAccountModel(
                    id="user-int-1",
                    email="integration-user@example.com",
                    display_name="Integration user",
                    status="active",
                ),
            )
            await session.commit()

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
        ) as client:
            response = await client.get("/identity/users/integration-user@example.com")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "id": "user-int-1",
        "email": "integration-user@example.com",
        "display_name": "Integration user",
        "status": "active",
    }
