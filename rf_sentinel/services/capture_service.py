"""Servicio de capturas."""

from datetime import datetime

from ..database.models import Capture


class CaptureService:
    """Servicio para gestión de capturas."""

    def __init__(self):
        self.captures: list[Capture] = []

    async def create_capture(
        self, frequency: float, duration: float, sample_rate: float = 10e6
    ) -> Capture:
        capture = Capture(
            center_frequency=frequency,
            sample_rate=sample_rate,
            duration=duration,
            timestamp=datetime.utcnow(),
        )
        self.captures.append(capture)
        return capture

    async def get_capture(self, capture_id: int) -> Capture | None:
        for capture in self.captures:
            if capture.id == capture_id:
                return capture
        return None

    async def list_captures(self, limit: int = 100) -> list[Capture]:
        return self.captures[-limit:]

    async def delete_capture(self, capture_id: int) -> bool:
        for i, capture in enumerate(self.captures):
            if capture.id == capture_id:
                self.captures.pop(i)
                return True
        return False
