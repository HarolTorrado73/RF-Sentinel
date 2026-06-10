"""Búsqueda de picos."""

import numpy as np


class PeakFinder:
    """Busca picos en señales."""

    def __init__(self, threshold: float = -60.0, min_prominence: float = 5.0):
        self.threshold = threshold
        self.min_prominence = min_prominence

    def find_peaks(self, data: np.ndarray) -> list[tuple[int, float]]:
        """Encuentra picos en los datos."""
        peaks = []
        for i in range(1, len(data) - 1):
            if data[i] > self.threshold and data[i] > data[i - 1] and data[i] > data[i + 1]:
                prominence = data[i] - max(data[i - 1], data[i + 1])
                if prominence >= self.min_prominence:
                    peaks.append((int(i), float(data[i])))
        return peaks

    def find_frequency_peaks(
        self, spectrum: np.ndarray, frequencies: np.ndarray
    ) -> list[dict[str, float]]:
        """Encuentra picos con frecuencias."""
        peaks = self.find_peaks(spectrum)
        return [
            {"frequency": float(frequencies[idx]), "power": power, "index": idx}
            for idx, power in peaks
        ]
