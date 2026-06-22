"""Emergency stop watchdog."""

from collections.abc import Callable

from rf_sentinel.core.events import EVENT_SCAN_STARTED, EVENT_SCAN_STOPPED, EventBus


class Watchdog:
    """Monitor de seguridad con emergency stop."""

    def __init__(self, event_bus: EventBus, stop_callback: Callable | None = None):
        self.event_bus = event_bus
        self.stop_callback = stop_callback
        self._active = False
        self._subscribe()

    def _subscribe(self) -> None:
        self.event_bus.subscribe(EVENT_SCAN_STARTED, self._on_scan_started)
        self.event_bus.subscribe(EVENT_SCAN_STOPPED, self._on_scan_stopped)

    def _on_scan_started(self, _data: dict) -> None:
        self._active = True

    def _on_scan_stopped(self, _data: dict) -> None:
        self._active = False

    def emergency_stop(self) -> None:
        """Detiene todas las operaciones."""
        self._active = False
        if self.stop_callback:
            self.stop_callback()
