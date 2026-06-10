"""Sistema de plugins para RF Sentinel."""

from abc import ABC, abstractmethod
from typing import Any


class PluginBase(ABC):
    """Interfaz base para todos los plugins."""

    name: str = "base"
    version: str = "1.0.0"
    description: str = ""
    priority: int = 100

    @abstractmethod
    async def initialize(self) -> None:
        """Inicializa el plugin."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Limpia recursos del plugin."""
        pass

    @abstractmethod
    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        """Procesa datos con el plugin."""
        pass


class DetectionPlugin(PluginBase):
    """Plugin para detección de señales."""

    name = "detection_base"

    def detect(self, samples: bytes) -> list[dict[str, Any]]:
        raise NotImplementedError


class ClassificationPlugin(PluginBase):
    """Plugin para clasificación de señales."""

    name = "classification_base"

    def classify(self, signal: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class ExportPlugin(PluginBase):
    """Plugin para exportación de datos."""

    name = "export_base"

    def export(self, capture: dict[str, Any], format: str) -> bytes:
        raise NotImplementedError


# Registry de plugins
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
