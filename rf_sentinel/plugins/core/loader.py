"""Loader de plugins con auto-discovery."""

import importlib
import pkgutil

from rf_sentinel.plugins.core.base import PluginBase
from rf_sentinel.plugins.core.registry import register_plugin


def load_builtin_plugins() -> None:
    """Carga automáticamente todos los plugins builtin."""
    import rf_sentinel.plugins.builtin as builtin_pkg

    for _finder, name, _ispkg in pkgutil.iter_modules(builtin_pkg.__path__):
        if not name.startswith("_"):
            try:
                module = importlib.import_module(f"rf_sentinel.plugins.builtin.{name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, PluginBase)
                        and attr is not PluginBase
                    ):
                        register_plugin(attr.name, attr)
            except Exception:
                pass
