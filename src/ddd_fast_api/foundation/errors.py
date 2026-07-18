"""Foundation error types and FastAPI exception handling."""

from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


@dataclass(slots=True)
class ProjectError(Exception):
    """Base structured error for the template."""

    code: str
    message: str
    status_code: int = 400
    details: dict[str, Any] = field(default_factory=dict)

    def to_response(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "error": {
                "code": self.code,
                "message": self.message,
            }
        }
        if self.details:
            payload["error"]["details"] = self.details
        return payload


async def handle_project_error(_: Request, exc: Exception) -> JSONResponse:
    """Convert a project error into a stable API response."""

    assert isinstance(exc, ProjectError)

    return JSONResponse(status_code=exc.status_code, content=exc.to_response())


async def handle_unexpected_error(_: Request, __: Exception) -> JSONResponse:
    """Convert an unexpected exception into a stable internal error response."""

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_error",
                "message": "An unexpected error occurred.",
            }
        },
    )


def register_exception_handlers(application: FastAPI) -> None:
    """Register foundation exception handlers on the FastAPI application."""

    application.add_exception_handler(ProjectError, handle_project_error)
    application.add_exception_handler(Exception, handle_unexpected_error)
