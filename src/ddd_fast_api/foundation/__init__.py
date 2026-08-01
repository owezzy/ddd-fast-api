"""Foundation layer package.

Project-independent logging, telemetry, and utility helpers will live here.
"""

from ddd_fast_api.foundation.auth import (
    AuthenticatedPrincipal,
    Authenticator,
    HMACBearerAuthenticator,
)
from ddd_fast_api.foundation.errors import ProjectError, register_exception_handlers
from ddd_fast_api.foundation.logging import StructuredFormatter, configure_logging, get_logger
from ddd_fast_api.foundation.settings import Settings, get_settings
from ddd_fast_api.foundation.telemetry import Telemetry, TelemetrySnapshot

__all__ = [
    "ProjectError",
    "AuthenticatedPrincipal",
    "Authenticator",
    "HMACBearerAuthenticator",
    "Settings",
    "StructuredFormatter",
    "configure_logging",
    "get_logger",
    "get_settings",
    "register_exception_handlers",
    "Telemetry",
    "TelemetrySnapshot",
]
