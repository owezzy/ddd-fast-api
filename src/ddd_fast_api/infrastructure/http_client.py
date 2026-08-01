"""Resilient outbound HTTP adapter."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

import httpx


class ResilientHttpClient:
    """Async HTTP client with bounded retries for transient failures."""

    def __init__(
        self,
        *,
        timeout_seconds: float = 5.0,
        max_retries: int = 2,
        client: httpx.AsyncClient | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("Outbound timeout must be greater than zero.")
        if max_retries < 0:
            raise ValueError("Outbound max retries cannot be negative.")
        self._client = client or httpx.AsyncClient(timeout=timeout_seconds)
        self._owns_client = client is None
        self._max_retries = max_retries
        self._sleep = sleep

    async def request(
        self,
        method: str,
        url: str,
        *,
        idempotent: bool = False,
        **kwargs: Any,
    ) -> httpx.Response:
        attempts = self._max_retries + 1 if idempotent else 1
        for attempt in range(attempts):
            try:
                response = await self._client.request(method, url, **kwargs)
            except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
                if attempt == attempts - 1:
                    raise
                await self._sleep(2**attempt)
                continue

            if response.status_code not in {429, 500, 502, 503, 504}:
                return response
            if attempt == attempts - 1:
                return response
            await self._sleep(2**attempt)

        raise RuntimeError("Outbound request loop ended unexpectedly.")

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """Issue an idempotent GET request."""

        return await self.request("GET", url, idempotent=True, **kwargs)

    async def close(self) -> None:
        """Close the underlying client when this adapter owns it."""

        if self._owns_client:
            await self._client.aclose()
