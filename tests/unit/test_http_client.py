import httpx
import pytest

from ddd_fast_api.infrastructure.http_client import ResilientHttpClient


@pytest.mark.anyio
async def test_get_retries_transient_response_and_returns_success() -> None:
    responses = iter([httpx.Response(503), httpx.Response(200, json={"ok": True})])
    sleeps: list[float] = []

    async def handler(_: httpx.Request) -> httpx.Response:
        return next(responses)

    async def sleep(delay: float) -> None:
        sleeps.append(delay)

    client = ResilientHttpClient(
        max_retries=2,
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        sleep=sleep,
    )
    response = await client.get("https://example.test/resource")
    await client.close()

    assert response.status_code == 200
    assert sleeps == [1]


@pytest.mark.anyio
async def test_non_idempotent_request_is_not_retried_by_default() -> None:
    calls = 0

    async def handler(_: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503)

    client = ResilientHttpClient(
        max_retries=3,
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )
    response = await client.request("POST", "https://example.test/resource")
    await client.close()

    assert response.status_code == 503
    assert calls == 1
