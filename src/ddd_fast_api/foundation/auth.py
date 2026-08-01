"""Authentication primitives shared by HTTP adapters and tests."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import time
from collections.abc import Collection
from dataclasses import dataclass
from typing import Protocol, cast

from ddd_fast_api.foundation.errors import ProjectError


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal:
    """Identity and policy claims extracted from a validated credential."""

    subject: str
    roles: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()
    claims: dict[str, object] | None = None

    def has_permission(self, permission: str) -> bool:
        """Return whether this principal has a direct or role-derived permission."""

        return permission in self.permissions or "admin" in self.roles


class Authenticator(Protocol):
    """Port for adapters that turn transport credentials into principals."""

    def issue_token(
        self,
        subject: str,
        *,
        roles: Collection[str] = (),
        permissions: Collection[str] = (),
    ) -> str: ...

    def authenticate(self, authorization: str | None) -> AuthenticatedPrincipal: ...


def _encode_segment(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return base64.urlsafe_b64encode(payload).rstrip(b"=").decode()


def _decode_segment(value: str) -> object:
    padded = value + "=" * (-len(value) % 4)
    return json.loads(base64.urlsafe_b64decode(padded.encode()))


class HMACBearerAuthenticator:
    """Small HS256 adapter for local use and as a replaceable auth seam.

    Production deployments should replace this adapter with an OIDC/JWKS
    implementation. The wire format is standard three-segment JWT, so the
    route dependency does not need to change when the adapter changes.
    """

    def __init__(self, *, secret: str, audience: str, token_ttl_seconds: int = 900) -> None:
        if len(secret) < 16:
            raise ValueError("Authentication secret must contain at least 16 characters.")
        self._secret = secret.encode()
        self._audience = audience
        self._token_ttl_seconds = token_ttl_seconds

    def issue_token(
        self,
        subject: str,
        *,
        roles: Collection[str] = (),
        permissions: Collection[str] = (),
    ) -> str:
        if not subject.strip():
            raise ValueError("Token subject cannot be empty.")
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "aud": self._audience,
            "exp": int(time.time()) + self._token_ttl_seconds,
            "permissions": sorted(set(permissions)),
            "roles": sorted(set(roles)),
            "sub": subject.strip(),
        }
        signing_input = f"{_encode_segment(header)}.{_encode_segment(payload)}"
        signature = hmac.new(
            self._secret,
            signing_input.encode(),
            hashlib.sha256,
        ).digest()
        return f"{signing_input}.{base64.urlsafe_b64encode(signature).rstrip(b'=').decode()}"

    def authenticate(self, authorization: str | None) -> AuthenticatedPrincipal:
        if not authorization or not authorization.startswith("Bearer "):
            raise ProjectError(
                code="authentication_required",
                message="A valid bearer token is required.",
                status_code=401,
            )

        token = authorization[7:].strip()
        parts = token.split(".")
        if len(parts) != 3:
            raise self._invalid_token()

        signing_input = ".".join(parts[:2])
        expected = hmac.new(self._secret, signing_input.encode(), hashlib.sha256).digest()
        padded_signature = parts[2] + "=" * (-len(parts[2]) % 4)
        try:
            provided = base64.urlsafe_b64decode(padded_signature.encode())
            header = _decode_segment(parts[0])
            decoded_payload = _decode_segment(parts[1])
        except (ValueError, TypeError, binascii.Error, json.JSONDecodeError):
            raise self._invalid_token() from None

        if not isinstance(header, dict) or header.get("alg") != "HS256":
            raise self._invalid_token()
        if not hmac.compare_digest(provided, expected):
            raise self._invalid_token()
        if not isinstance(decoded_payload, dict):
            raise self._invalid_token()
        payload = cast(dict[str, object], decoded_payload)
        expiration = payload.get("exp", 0)
        if payload.get("aud") != self._audience or not isinstance(expiration, int):
            raise self._invalid_token()
        if expiration <= int(time.time()):
            raise self._invalid_token()

        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject:
            raise self._invalid_token()
        return AuthenticatedPrincipal(
            subject=subject,
            roles=tuple(str(role) for role in cast(list[object], payload.get("roles", []))),
            permissions=tuple(
                str(permission) for permission in cast(list[object], payload.get("permissions", []))
            ),
            claims=payload,
        )

    @staticmethod
    def _invalid_token() -> ProjectError:
        return ProjectError(
            code="invalid_bearer_token",
            message="The bearer token is invalid or expired.",
            status_code=401,
        )
