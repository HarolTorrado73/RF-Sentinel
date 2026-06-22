"""Servicio de capturas."""

from datetime import datetime

from rf_sentinel.database.models.capture import Capture
from rf_sentinel.database.repositories.capture_repo import CaptureRepository
from rf_sentinel.database.repositories.signal_repo import SignalRepository


class CaptureService:
    """Servicio para gestión de capturas."""

    def __init__(
        self,
        capture_repo: CaptureRepository | None = None,
        signal_repo: SignalRepository | None = None,
    ):
        self.capture_repo = capture_repo
        self.signal_repo = signal_repo
        self.captures: list[Capture] = []
        self._next_id = 1

    async def create_capture(
        self, frequency: float, duration: float, sample_rate: float = 10e6
    ) -> Capture:
        capture = Capture(
            center_frequency=frequency,
            sample_rate=sample_rate,
            duration=duration,
            timestamp=datetime.utcnow(),
        )
        if not self.capture_repo:
            capture.id = self._next_id
            self._next_id += 1
        self.captures.append(capture)
        if self.capture_repo:
            capture = await self.capture_repo.create(capture)
        return capture

    async def get_capture(self, capture_id: int) -> Capture | None:
        if self.capture_repo:
            return await self.capture_repo.get(capture_id)
        for capture in self.captures:
            if capture.id == capture_id:
                return capture
        return None

    async def list_captures(self, limit: int = 100) -> list[Capture]:
        if self.capture_repo:
            return await self.capture_repo.list(limit=limit)
        return self.captures[-limit:]

    async def delete_capture(self, capture_id: int) -> bool:
        if self.capture_repo:
            return await self.capture_repo.delete(capture_id)
        for i, capture in enumerate(self.captures):
            if capture.id == capture_id:
                self.captures.pop(i)
                return True
        return False
