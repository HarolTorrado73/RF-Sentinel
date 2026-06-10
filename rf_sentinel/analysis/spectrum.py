"""Análisis de espectro."""

import numpy as np


class SpectrumAnalyzer:
    """Analizador de espectro en tiempo real."""

    def __init__(self, sample_rate: float = 10e6, fft_size: int = 1024):
        self.sample_rate = sample_rate
        self.fft_size = fft_size
        self._window = np.hanning(fft_size)

    def analyze(self, samples: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Procesa muestras y retorna espectro."""
        if len(samples) < self.fft_size:
            samples = np.pad(samples, (0, self.fft_size - len(samples)))

        fft = np.fft.fft(samples * self._window)
        psd = np.abs(fft[: self.fft_size // 2]) ** 2
        psd_db = 10 * np.log10(psd + 1e-10)

        frequencies = np.fft.fftfreq(self.fft_size, 1 / self.sample_rate)[: self.fft_size // 2]

        return psd_db, np.abs(frequencies)

    def detect_peaks(
        self, spectrum: np.ndarray, threshold: float = -60.0, min_distance: int = 10
    ) -> list[int]:
        """Detecta picos en el espectro."""
        peaks = []
        for i in range(min_distance, len(spectrum) - min_distance):
            if spectrum[i] > threshold:
                is_peak = all(
                    spectrum[i] >= spectrum[j]
                    for j in range(i - min_distance, i + min_distance + 1)
                )
                if is_peak:
                    peaks.append(i)
        return peaks
