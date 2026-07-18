"""Foundation layer package.

Project-independent logging, telemetry, and utility helpers will live here.
"""

from ddd_fast_api.foundation.errors import ProjectError, register_exception_handlers
from ddd_fast_api.foundation.settings import Settings, get_settings

__all__ = ["ProjectError", "Settings", "get_settings", "register_exception_handlers"]
