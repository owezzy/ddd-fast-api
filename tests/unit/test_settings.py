"""Tests for foundation settings."""

import pytest

from ddd_fast_api.foundation.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "ddd-fast-api"
    assert settings.app_env == "development"
    assert settings.app_debug is False
    assert settings.app_host == "127.0.0.1"
    assert settings.app_port == 8000


def test_settings_allow_environment_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DDD_FAST_API_APP_NAME", "custom-template")
    monkeypatch.setenv("DDD_FAST_API_APP_ENV", "test")
    monkeypatch.setenv("DDD_FAST_API_APP_DEBUG", "true")
    monkeypatch.setenv("DDD_FAST_API_APP_HOST", "0.0.0.0")
    monkeypatch.setenv("DDD_FAST_API_APP_PORT", "9000")

    settings = Settings(_env_file=None)

    assert settings.app_name == "custom-template"
    assert settings.app_env == "test"
    assert settings.app_debug is True
    assert settings.app_host == "0.0.0.0"
    assert settings.app_port == 9000
