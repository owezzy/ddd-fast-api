"""Tests for foundation error handling."""

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from ddd_fast_api.foundation import ProjectError, register_exception_handlers


def create_error_app() -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/project-error")
    def project_error() -> None:
        raise ProjectError(
            code="scaffold_error",
            message="Scaffold error occurred.",
            status_code=418,
            details={"stage": "foundation"},
        )

    @app.get("/unexpected-error")
    def unexpected_error() -> None:
        raise RuntimeError("boom")

    return app


@pytest.mark.anyio
async def test_project_error_response_shape() -> None:
    app = create_error_app()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/project-error")

    assert response.status_code == 418
    assert response.json() == {
        "error": {
            "code": "scaffold_error",
            "message": "Scaffold error occurred.",
            "details": {"stage": "foundation"},
        }
    }


@pytest.mark.anyio
async def test_unexpected_error_response_shape() -> None:
    app = create_error_app()

    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/unexpected-error")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_error",
            "message": "An unexpected error occurred.",
        }
    }
