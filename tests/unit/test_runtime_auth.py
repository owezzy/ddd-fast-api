import pytest
from httpx import ASGITransport, AsyncClient

from ddd_fast_api.bootstrap import create_app
from ddd_fast_api.foundation import HMACBearerAuthenticator, ProjectError, Settings


def test_hmac_authenticator_round_trips_principal_claims() -> None:
    authenticator = HMACBearerAuthenticator(secret="a" * 32, audience="test")
    token = authenticator.issue_token(
        "user-1",
        roles=["operator"],
        permissions=["catalog:read"],
    )

    principal = authenticator.authenticate(f"Bearer {token}")

    assert principal.subject == "user-1"
    assert principal.roles == ("operator",)
    assert principal.permissions == ("catalog:read",)
    assert principal.has_permission("catalog:read") is True
    assert principal.has_permission("catalog:manage") is False


def test_hmac_authenticator_rejects_tampered_token() -> None:
    authenticator = HMACBearerAuthenticator(secret="a" * 32, audience="test")
    token = authenticator.issue_token("user-1")

    with pytest.raises(ProjectError) as error:
        authenticator.authenticate(f"Bearer {token[:-1]}x")

    assert getattr(error.value, "code") == "invalid_bearer_token"


@pytest.mark.anyio
async def test_protected_routes_require_and_enforce_permissions() -> None:
    app = create_app(Settings(_env_file=None, database_url="sqlite+aiosqlite:///:memory:"))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        missing = await client.get("/identity/me")
        token_response = await client.post(
            "/auth/dev-token",
            json={"subject": "user-1", "permissions": ["catalog:read"]},
        )
        token = token_response.json()["access_token"]
        forbidden = await client.get(
            "/catalog/management-preview",
            headers={"Authorization": f"Bearer {token}"},
        )
        allowed_token = await client.post(
            "/auth/dev-token",
            json={"subject": "admin-1", "roles": ["admin"]},
        )
        allowed = await client.get(
            "/catalog/management-preview",
            headers={"Authorization": f"Bearer {allowed_token.json()['access_token']}"},
        )

    assert missing.status_code == 401
    assert token_response.status_code == 200
    assert forbidden.status_code == 403
    assert allowed.status_code == 200
    assert allowed.json()["subject"] == "admin-1"
