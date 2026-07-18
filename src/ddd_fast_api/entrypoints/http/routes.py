"""Minimal HTTP routes for the first executable scaffold."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["meta"])
def root() -> dict[str, str]:
    """Describe the current state of the project."""

    return {
        "name": "ddd-fast-api",
        "status": "foundation-scaffold",
        "message": "The first executable foundation slice is in place.",
    }


@router.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    """Simple health endpoint for local validation."""

    return {"status": "ok"}
