"""Application bootstrap for the initial foundation slice."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from ddd_fast_api.entrypoints.http.routes import router
from ddd_fast_api.entrypoints.http.telemetry import RequestTelemetryMiddleware
from ddd_fast_api.foundation import (
    HMACBearerAuthenticator,
    Settings,
    Telemetry,
    configure_logging,
    get_logger,
    get_settings,
    register_exception_handlers,
)
from ddd_fast_api.infrastructure.http_client import ResilientHttpClient
from ddd_fast_api.infrastructure.persistence import (
    create_engine,
    create_session_factory_from_engine,
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Own shared process resources for the current application instance."""

    settings = application.state.settings
    engine = create_engine(settings)
    session_factory = create_session_factory_from_engine(engine)
    http_client = ResilientHttpClient(
        timeout_seconds=settings.outbound_timeout_seconds,
        max_retries=settings.outbound_max_retries,
    )

    application.state.engine = engine
    application.state.session_factory = session_factory
    application.state.http_client = http_client
    application.state.startup_complete = True
    application.state.ready = True

    logger.info(
        "persistence resources initialized",
        extra={"event": "persistence_resources_initialized"},
    )

    yield

    await engine.dispose()
    await http_client.close()
    application.state.ready = False
    logger.info(
        "persistence resources disposed",
        extra={"event": "persistence_resources_disposed"},
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    """Construct the FastAPI application for the current scaffold."""

    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings)

    application = FastAPI(
        title=resolved_settings.app_name,
        version="0.1.0",
        summary="Pragmatic DDD FastAPI template scaffold",
        description=(
            "Initial executable foundation slice for an Ardan-inspired FastAPI service template."
        ),
        debug=resolved_settings.app_debug,
        lifespan=lifespan,
    )
    application.state.settings = resolved_settings
    application.state.telemetry = Telemetry()
    application.state.authenticator = HMACBearerAuthenticator(
        secret=resolved_settings.auth_secret,
        audience=resolved_settings.auth_audience,
        token_ttl_seconds=resolved_settings.auth_token_ttl_seconds,
    )
    application.state.startup_complete = False
    application.state.ready = False
    application.add_middleware(RequestTelemetryMiddleware, telemetry=application.state.telemetry)
    register_exception_handlers(application)
    application.include_router(router)
    logger.info(
        "application created",
        extra={"event": "application_created"},
    )
    return application


app = create_app()


def run() -> None:
    """Run the local development server."""

    settings = get_settings()
    logger.info(
        "starting uvicorn",
        extra={
            "event": "server_starting",
            "host": settings.app_host,
            "port": settings.app_port,
        },
    )

    uvicorn.run(
        "ddd_fast_api.bootstrap:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=False,
    )
