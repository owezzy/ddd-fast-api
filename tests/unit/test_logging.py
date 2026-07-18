"""Tests for structured logging configuration."""

from __future__ import annotations

import json
import logging

from ddd_fast_api.foundation import Settings, StructuredFormatter, configure_logging


def test_structured_formatter_renders_expected_fields() -> None:
    formatter = StructuredFormatter(app_name="ddd-fast-api", app_env="test")

    record = logging.LogRecord(
        name="ddd_fast_api.tests",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="hello world",
        args=(),
        exc_info=None,
    )
    record.event = "test_event"

    payload = json.loads(formatter.format(record))

    assert payload["app"] == "ddd-fast-api"
    assert payload["environment"] == "test"
    assert payload["event"] == "test_event"
    assert payload["level"] == "INFO"
    assert payload["logger"] == "ddd_fast_api.tests"
    assert payload["message"] == "hello world"
    assert "timestamp" in payload


def test_configure_logging_sets_root_logger_level() -> None:
    settings = Settings(_env_file=None, app_log_level="DEBUG")

    configure_logging(settings)

    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG
    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0].formatter, StructuredFormatter)
