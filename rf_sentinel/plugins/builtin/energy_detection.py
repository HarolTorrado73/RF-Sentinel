"""Plugin de detección por energía."""

from typing import Any

import numpy as np

from rf_sentinel.detection.energy import EnergyDetector
from rf_sentinel.plugins.core.base import DetectionPlugin


class EnergyDetectionPlugin(DetectionPlugin):
    """Detección de señales basada en umbral de energía."""

    name = "energy_detection"
    version = "1.0.0"
    description = "Detección de picos por umbral de energía"

    def __init__(self, threshold_db: float = -60.0, min_bandwidth: float = 10e3):
        self.threshold_db = threshold_db
        self.min_bandwidth = min_bandwidth
        self._initialized = False
        self._detector = EnergyDetector(threshold_db=threshold_db, window_size=1024)

    async def initialize(self) -> None:
        self._initialized = True

    async def cleanup(self) -> None:
        self._initialized = False
        self._detector = EnergyDetector()

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        if not self._initialized:
            raise RuntimeError("Plugin not initialized")
        return data

    def detect(self, samples: bytes) -> list[dict[str, Any]]:
        """Detecta señales usando detección de energía."""
        if not self._initialized:
            raise RuntimeError("Plugin not initialized")
        iq_data = np.frombuffer(samples, dtype=np.complex64)
        return self._detector.detect(iq_data)[:10]
