"""Registry de plugins."""

from rf_sentinel.plugins.core.base import PluginBase

_plugins: dict[str, type[PluginBase]] = {}


def register_plugin(name: str, plugin_class: type[PluginBase]) -> None:
    """Registra un plugin."""
    _plugins[name] = plugin_class


def get_plugin(name: str) -> type[PluginBase] | None:
    """Obtiene un plugin por nombre."""
    return _plugins.get(name)


def list_plugins() -> list[str]:
    """Lista todos los plugins registrados."""
    return list(_plugins.keys())
