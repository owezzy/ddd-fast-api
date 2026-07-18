"""Transport schemas for metadata endpoints."""

from pydantic import BaseModel


class RootResponse(BaseModel):
    """Response for the scaffold metadata endpoint."""

    name: str
    status: str
    message: str


class HealthResponse(BaseModel):
    """Response for the health endpoint."""

    status: str
