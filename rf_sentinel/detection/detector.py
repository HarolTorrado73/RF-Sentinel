"""Detector principal de señales."""

import numpy as np


class SignalDetector:
    """Detector de señales con algoritmos configurables."""

    def __init__(self, threshold: float = -60.0, min_width: int = 10):
        self.threshold = threshold
        self.min_width = min_width

    def detect(self, spectrum: np.ndarray, frequencies: np.ndarray) -> list[dict[str, float]]:
        """Detecta picos en el espectro."""
        peaks = []
        above_threshold = spectrum > self.threshold

        for i in range(len(spectrum)):
            if above_threshold[i]:
                left = i
                while left > 0 and above_threshold[left - 1]:
                    left -= 1
                right = i
                while right < len(spectrum) - 1 and above_threshold[right + 1]:
                    right += 1

                width = right - left + 1
                if width >= self.min_width:
                    peak_power = float(np.max(spectrum[left : right + 1]))
                    peak_idx = int(np.argmax(spectrum[left : right + 1]) + left)
                    peaks.append(
                        {
                            "frequency": float(frequencies[peak_idx]),
                            "power": peak_power,
                            "bandwidth": float(frequencies[right] - frequencies[left]),
                        }
                    )

        return peaks
