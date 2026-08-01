"""Transport schemas for runtime platform capabilities."""

from pydantic import BaseModel, Field

from ddd_fast_api.foundation import AuthenticatedPrincipal


class HealthStatusResponse(BaseModel):
    """Machine-readable process health state."""

    status: str


class DevTokenRequest(BaseModel):
    """Development-only token request for exercising protected examples."""

    subject: str = Field(min_length=1)
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)


class TokenResponse(BaseModel):
    """Bearer token returned by the local development helper."""

    access_token: str
    token_type: str = "bearer"


class PrincipalResponse(BaseModel):
    """Safe representation of an authenticated principal."""

    subject: str
    roles: list[str]
    permissions: list[str]

    @classmethod
    def from_principal(cls, principal: AuthenticatedPrincipal) -> "PrincipalResponse":
        return cls(
            subject=principal.subject,
            roles=list(principal.roles),
            permissions=list(principal.permissions),
        )
