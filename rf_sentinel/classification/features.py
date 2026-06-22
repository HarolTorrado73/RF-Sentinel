"""Extracción de características de señales."""

from typing import Any

import numpy as np


class FeatureExtractor:
    """Extrae características de señales para ML."""

    def __init__(self, sample_rate: float = 10e6):
        self.sample_rate = sample_rate

    def extract(self, samples: np.ndarray) -> dict[str, Any]:
        """Extrae features de la señal."""
        return {
            "mean_power": float(np.mean(np.abs(samples) ** 2)),
            "std_power": float(np.std(np.abs(samples) ** 2)),
            "peak_power": float(np.max(np.abs(samples) ** 2)),
            "bandwidth": float(self._estimate_bandwidth(samples)),
            "spectral_flatness": float(self._spectral_flatness(samples)),
            "center_frequency": float(len(samples) // 2),
        }

    def _estimate_bandwidth(self, samples: np.ndarray) -> float:
        """Estima ancho de banda en Hz."""
        fft = np.fft.fft(samples)
        psd = np.abs(fft) ** 2
        threshold = np.max(psd) * 0.1
        significant_bins = np.where(psd > threshold)[0]
        if len(significant_bins) == 0:
            return 0.0
        bin_width = self.sample_rate / len(samples)
        return float((significant_bins[-1] - significant_bins[0]) * bin_width)

    def _spectral_flatness(self, samples: np.ndarray) -> float:
        """Calcula spectral flatness."""
        fft = np.fft.fft(samples)
        psd = np.abs(fft) ** 2 + 1e-10
        geometric = np.exp(np.mean(np.log(psd)))
        arithmetic = np.mean(psd)
        return float(geometric / arithmetic)
