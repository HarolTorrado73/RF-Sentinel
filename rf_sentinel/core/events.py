"""Event bus para comunicación interna entre módulos."""

from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    """Bus de eventos pub/sub interno."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """Suscribe un callback a un evento."""
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """Desuscribe un callback de un evento."""
        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def publish(self, event_name: str, data: dict[str, Any]) -> None:
        """Publica un evento a todos los suscriptores."""
        for callback in self._subscribers.get(event_name, []):
            callback(data)


# Eventos estándar
EVENT_SCAN_STARTED = "scan.started"
EVENT_SCAN_STOPPED = "scan.stopped"
EVENT_SCAN_PROGRESS = "scan.progress"
EVENT_SIGNAL_DETECTED = "signal.detected"
EVENT_CAPTURE_CREATED = "capture.created"
EVENT_CAPTURE_EXPORTED = "capture.exported"
EVENT_DEVICE_CONNECTED = "device.connected"
EVENT_DEVICE_DISCONNECTED = "device.disconnected"
