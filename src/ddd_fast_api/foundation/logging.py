"""Structured logging for the foundation phase."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from ddd_fast_api.foundation.settings import Settings


class StructuredFormatter(logging.Formatter):
    """Render log records as stable JSON objects."""

    def __init__(self, *, app_name: str, app_env: str) -> None:
        super().__init__()
        self.app_name = app_name
        self.app_env = app_env

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "app": self.app_name,
            "environment": self.app_env,
        }

        for key in ("event", "host", "port"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, sort_keys=True)


def configure_logging(settings: Settings) -> None:
    """Configure root logging for the current scaffold."""

    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(
        StructuredFormatter(app_name=settings.app_name, app_env=settings.app_env),
    )

    root_logger.addHandler(handler)
    root_logger.setLevel(settings.app_log_level.upper())


def get_logger(name: str) -> logging.Logger:
    """Return a logger for a module or subsystem."""

    return logging.getLogger(name)
