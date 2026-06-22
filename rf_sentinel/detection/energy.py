"""Detección por energía."""

import numpy as np

from rf_sentinel.detection.base import Detector


class EnergyDetector(Detector):
    """Detector de energía para señales."""

    def __init__(self, threshold_db: float = -60.0, window_size: int = 1024):
        self.threshold_db = threshold_db
        self.window_size = window_size

    def detect(
        self, samples: np.ndarray, frequencies: np.ndarray | None = None
    ) -> list[dict[str, float]]:
        """Detecta picos de energía."""
        if len(samples) < self.window_size:
            return []

        detections = []
        for i in range(0, len(samples) - self.window_size, self.window_size // 2):
            window = samples[i : i + self.window_size]
            power = 10 * np.log10(np.mean(np.abs(window) ** 2) + 1e-10)

            if power > self.threshold_db:
                freq = (
                    float(frequencies[i]) if frequencies is not None else float(i)
                )
                detections.append(
                    {
                        "frequency": freq,
                        "power": float(power),
                        "bandwidth": float(self.window_size),
                    }
                )

        return detections
