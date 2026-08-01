"""Request telemetry middleware at the HTTP boundary."""

from __future__ import annotations

from typing import cast
from uuid import uuid4

from starlette.types import ASGIApp, Message, Receive, Scope, Send

from ddd_fast_api.foundation import Telemetry, get_logger

logger = get_logger(__name__)


class RequestTelemetryMiddleware:
    """Attach correlation identifiers and record response status counters."""

    def __init__(self, app: ASGIApp, telemetry: Telemetry) -> None:
        self.app = app
        self.telemetry = telemetry

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = _header_value(scope, b"x-request-id") or str(uuid4())
        trace_id = _header_value(scope, b"x-trace-id") or str(uuid4())
        scope["state"] = {**scope.get("state", {}), "request_id": request_id, "trace_id": trace_id}
        status_code = 500

        async def send_with_telemetry(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
                headers = list(message.get("headers", []))
                headers.extend(
                    [
                        (b"x-request-id", request_id.encode()),
                        (b"x-trace-id", trace_id.encode()),
                    ]
                )
                message = {**message, "headers": headers}
            await send(message)

        try:
            await self.app(scope, receive, send_with_telemetry)
        finally:
            self.telemetry.record_request(status_code)
            logger.info(
                "http request completed",
                extra={
                    "event": "http_request_completed",
                    "request_id": request_id,
                    "trace_id": trace_id,
                    "status_code": status_code,
                },
            )


def _header_value(scope: Scope, name: bytes) -> str | None:
    for key, value in scope.get("headers", []):
        if key.lower() == name:
            return cast(bytes, value).decode("latin-1")
    return None
