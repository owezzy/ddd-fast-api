"""Dependency-free telemetry primitives for the service edges."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from threading import Lock


@dataclass(frozen=True, slots=True)
class TelemetrySnapshot:
    """Point-in-time request counters."""

    requests_total: int
    responses_by_status: dict[int, int]


class Telemetry:
    """Small metrics port that can later be backed by Prometheus/OpenTelemetry."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._requests_total = 0
        self._responses_by_status: Counter[int] = Counter()

    def record_request(self, status_code: int) -> None:
        with self._lock:
            self._requests_total += 1
            self._responses_by_status[status_code] += 1

    def snapshot(self) -> TelemetrySnapshot:
        with self._lock:
            return TelemetrySnapshot(
                requests_total=self._requests_total,
                responses_by_status=dict(self._responses_by_status),
            )

    def render_prometheus(self) -> str:
        snapshot = self.snapshot()
        lines = [
            "# HELP ddd_fast_api_http_requests_total Total HTTP requests.",
            "# TYPE ddd_fast_api_http_requests_total counter",
            f"ddd_fast_api_http_requests_total {snapshot.requests_total}",
            "# HELP ddd_fast_api_http_responses_total HTTP responses by status code.",
            "# TYPE ddd_fast_api_http_responses_total counter",
        ]
        lines.extend(
            f'ddd_fast_api_http_responses_total{{status_code="{status}"}} {count}'
            for status, count in sorted(snapshot.responses_by_status.items())
        )
        return "\n".join(lines) + "\n"
