"""Extracción de características de señales."""

from typing import Any

import numpy as np


class FeatureExtractor:
    """Extrae características de señales para ML."""

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
        """Estima ancho de banda."""
        fft = np.fft.fft(samples)
        psd = np.abs(fft) ** 2
        threshold = np.max(psd) * 0.1
        return float(np.sum(psd > threshold))

    def _spectral_flatness(self, samples: np.ndarray) -> float:
        """Calcula spectral flatness."""
        fft = np.fft.fft(samples)
        psd = np.abs(fft) ** 2 + 1e-10
        geometric = np.exp(np.mean(np.log(psd)))
        arithmetic = np.mean(psd)
        return float(geometric / arithmetic)
