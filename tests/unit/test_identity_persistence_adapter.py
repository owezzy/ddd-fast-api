"""Tests for the SQLAlchemy-backed identity repository adapter."""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from ddd_fast_api.domain.identity import EmailAddress, UserAccountStatus
from ddd_fast_api.foundation import Settings
from ddd_fast_api.infrastructure.persistence import (
    Base,
    SQLAlchemyIdentityRepository,
    create_engine,
)
from ddd_fast_api.infrastructure.persistence.models import UserAccountModel


@pytest.mark.anyio
async def test_sqlalchemy_identity_repository_gets_account_by_email() -> None:
    settings = Settings(_env_file=None, database_url="sqlite+aiosqlite:///:memory:")
    engine = create_engine(settings)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        session.add(
            UserAccountModel(
                id="user-1",
                email="user@example.com",
                display_name="Starter user",
                status="active",
            ),
        )
        await session.commit()

    async with session_factory() as session:
        repository = SQLAlchemyIdentityRepository(session)
        account = await repository.get_account_by_email(EmailAddress("USER@example.com"))
        missing = await repository.get_account_by_email(EmailAddress("missing@example.com"))

    assert account is not None
    assert account.id == "user-1"
    assert account.display_name == "Starter user"
    assert account.status is UserAccountStatus.ACTIVE
    assert missing is None

    await engine.dispose()
