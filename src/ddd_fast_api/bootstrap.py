"""Application bootstrap for the initial foundation slice."""

import uvicorn
from fastapi import FastAPI

from ddd_fast_api.entrypoints.http.routes import router
from ddd_fast_api.foundation import Settings, get_settings, register_exception_handlers


def create_app(settings: Settings | None = None) -> FastAPI:
    """Construct the FastAPI application for the current scaffold."""

    resolved_settings = settings or get_settings()

    application = FastAPI(
        title=resolved_settings.app_name,
        version="0.1.0",
        summary="Pragmatic DDD FastAPI template scaffold",
        description=(
            "Initial executable foundation slice for an Ardan-inspired FastAPI service template."
        ),
        debug=resolved_settings.app_debug,
    )
    register_exception_handlers(application)
    application.include_router(router)
    return application


app = create_app()


def run() -> None:
    """Run the local development server."""

    settings = get_settings()

    uvicorn.run(
        "ddd_fast_api.bootstrap:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=False,
    )
