"""Plugin de detección por energía."""

from typing import Any

import numpy as np

from .. import DetectionPlugin


class EnergyDetectionPlugin(DetectionPlugin):
    """Detección de señales basada en umbral de energía."""

    name = "energy_detection"
    version = "1.0.0"
    description = "Detección de picos por umbral de energía"

    def __init__(self, threshold_db: float = -60.0, min_bandwidth: float = 10e3):
        self.threshold_db = threshold_db
        self.min_bandwidth = min_bandwidth
        self._initialized = False

    async def initialize(self) -> None:
        self._initialized = True

    async def cleanup(self) -> None:
        self._initialized = False

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        if not self._initialized:
            raise RuntimeError("Plugin not initialized")
        return data

    def detect(self, samples: bytes) -> list[dict[str, Any]]:
        """Detecta señales usando detección de energía."""
        # Convert bytes to numpy array
        iq_data = np.frombuffer(samples, dtype=np.complex64)

        # Power spectral density
        psd = np.abs(np.fft.fft(iq_data)) ** 2
        psd_db = 10 * np.log10(psd + 1e-10)

        # Find peaks above threshold
        peaks = []

        for i, power in enumerate(psd_db):
            if power > self.threshold_db:
                frequency = i  # Simplified
                peaks.append(
                    {
                        "frequency": float(frequency),
                        "bandwidth": self.min_bandwidth,
                        "power": float(power),
                    }
                )

        return peaks[:10]  # Max 10 peaks
