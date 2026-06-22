"""Servicio de escaneo."""

from typing import Any

from rf_sentinel.database.repositories.capture_repo import CaptureRepository
from rf_sentinel.database.repositories.signal_repo import SignalRepository


class ScanService:
    """Servicio para gestión de escaneos."""

    def __init__(
        self,
        capture_repo: CaptureRepository | None = None,
        signal_repo: SignalRepository | None = None,
    ):
        self.capture_repo = capture_repo
        self.signal_repo = signal_repo
        self.scans: dict[str, dict[str, Any]] = {}

    async def start_scan(self, start_freq: float, stop_freq: float, step: float = 1e6) -> str:
        scan_id = f"scan_{len(self.scans)}"
        self.scans[scan_id] = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "step": step,
            "status": "running",
            "progress": 0.0,
        }
        return scan_id

    async def get_status(self, scan_id: str) -> dict[str, Any]:
        return self.scans.get(scan_id, {"status": "not_found"})

    async def stop_scan(self, scan_id: str) -> None:
        if scan_id in self.scans:
            self.scans[scan_id]["status"] = "stopped"
