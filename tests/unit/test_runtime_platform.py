import pytest
from httpx import ASGITransport, AsyncClient

from ddd_fast_api.bootstrap import create_app
from ddd_fast_api.foundation import Settings


@pytest.mark.anyio
async def test_health_states_transition_with_lifespan() -> None:
    app = create_app(Settings(_env_file=None, database_url="sqlite+aiosqlite:///:memory:"))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        before_startup = await client.get("/health/startup")
        before_ready = await client.get("/health/ready")

    async with app.router.lifespan_context(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
        ) as client:
            live = await client.get("/health/live")
            startup = await client.get("/health/startup")
            ready = await client.get("/health/ready")

    assert before_startup.status_code == 503
    assert before_ready.status_code == 503
    assert live.json() == {"status": "live"}
    assert startup.json() == {"status": "started"}
    assert ready.json() == {"status": "ready"}


@pytest.mark.anyio
async def test_telemetry_preserves_request_ids_and_records_metrics() -> None:
    app = create_app(Settings(_env_file=None, database_url="sqlite+aiosqlite:///:memory:"))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(
            "/",
            headers={"X-Request-ID": "request-1", "X-Trace-ID": "trace-1"},
        )
        metrics = await client.get("/metrics")

    assert response.headers["x-request-id"] == "request-1"
    assert response.headers["x-trace-id"] == "trace-1"
    assert "ddd_fast_api_http_requests_total 1" in metrics.text
    assert 'ddd_fast_api_http_responses_total{status_code="200"} 1' in metrics.text
