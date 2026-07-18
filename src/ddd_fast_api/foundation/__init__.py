"""Foundation layer package.

Project-independent logging, telemetry, and utility helpers will live here.
"""

from ddd_fast_api.foundation.errors import ProjectError, register_exception_handlers
from ddd_fast_api.foundation.logging import StructuredFormatter, configure_logging, get_logger
from ddd_fast_api.foundation.settings import Settings, get_settings

__all__ = [
    "ProjectError",
    "Settings",
    "StructuredFormatter",
    "configure_logging",
    "get_logger",
    "get_settings",
    "register_exception_handlers",
]
