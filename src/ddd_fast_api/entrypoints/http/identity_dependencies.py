"""Dependency providers for the sample identity HTTP endpoint."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from ddd_fast_api.application.identity import GetUserAccountByEmail
from ddd_fast_api.domain.identity import IdentityRepository
from ddd_fast_api.entrypoints.http.identity_memory import build_sample_identity_repository
from ddd_fast_api.foundation import Settings, get_settings
from ddd_fast_api.infrastructure.persistence import (
    SQLAlchemyIdentityRepository,
    create_engine,
    create_session_factory_from_engine,
)


def _resolve_persistence_resources(
    request: Request,
    settings: Settings,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession], bool]:
    app_state = request.app.state
    state_settings = getattr(app_state, "settings", None)
    state_engine = getattr(app_state, "engine", None)
    state_session_factory = getattr(app_state, "session_factory", None)

    if (
        state_settings is not None
        and state_engine is not None
        and state_session_factory is not None
        and state_settings.database_url == settings.database_url
    ):
        return state_engine, state_session_factory, False

    engine = create_engine(settings)
    session_factory = create_session_factory_from_engine(engine)
    return engine, session_factory, True


async def get_identity_repository(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> AsyncIterator[IdentityRepository]:
    """Select the identity repository implementation for the current request."""

    if settings.identity_repository_backend == "memory":
        yield build_sample_identity_repository()
        return

    engine, session_factory, should_dispose_engine = _resolve_persistence_resources(
        request,
        settings,
    )

    async with session_factory() as session:
        yield SQLAlchemyIdentityRepository(session)

    if should_dispose_engine:
        await engine.dispose()


def get_user_account_by_email_use_case(
    repository: Annotated[IdentityRepository, Depends(get_identity_repository)],
) -> GetUserAccountByEmail:
    """Build the sample identity detail use case for the current scaffold."""

    return GetUserAccountByEmail(repository=repository)
