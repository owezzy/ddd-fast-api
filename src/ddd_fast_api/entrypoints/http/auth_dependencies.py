"""HTTP authentication and authorization dependencies."""

from collections.abc import Callable
from typing import cast

from fastapi import Depends, Header, Request

from ddd_fast_api.foundation import AuthenticatedPrincipal, Authenticator, ProjectError


def get_authenticator(request: Request) -> Authenticator:
    """Return the authenticator selected by the composition root."""

    return cast(Authenticator, request.app.state.authenticator)


def get_current_principal(
    authenticator: Authenticator = Depends(get_authenticator),
    authorization: str | None = Header(default=None),
) -> AuthenticatedPrincipal:
    """Authenticate the request's bearer credential."""

    return authenticator.authenticate(authorization)


def require_permission(permission: str) -> Callable[..., AuthenticatedPrincipal]:
    """Build a dependency enforcing one application policy permission."""

    def dependency(
        principal: AuthenticatedPrincipal = Depends(get_current_principal),
    ) -> AuthenticatedPrincipal:
        if not principal.has_permission(permission):
            raise ProjectError(
                code="forbidden",
                message="The authenticated principal lacks the required permission.",
                status_code=403,
                details={"permission": permission},
            )
        return principal

    return dependency
