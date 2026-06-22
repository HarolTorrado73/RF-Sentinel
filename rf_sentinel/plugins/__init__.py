"""Alias de compatibilidad: rf_sentinel.plugins → rf_sentinel.plugins.core + builtin."""

from rf_sentinel.plugins.core.base import (  # noqa: F401
    ClassificationPlugin,
    DetectionPlugin,
    ExportPlugin,
    PluginBase,
)
from rf_sentinel.plugins.core.registry import (  # noqa: F401
    get_plugin,
    list_plugins,
    register_plugin,
)

__all__ = [
    "PluginBase",
    "DetectionPlugin",
    "ClassificationPlugin",
    "ExportPlugin",
    "register_plugin",
    "get_plugin",
    "list_plugins",
]
