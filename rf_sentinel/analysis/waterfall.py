"""Waterfall para visualización de espectro en tiempo."""

import numpy as np


class Waterfall:
    """Generador de waterfall."""

    def __init__(self, width: int = 1024, height: int = 256):
        self.width = width
        self.height = height
        self._data = np.zeros((height, width), dtype=np.float32)
        self._index = 0

    def add_spectrum(self, spectrum: np.ndarray) -> None:
        """Añade una línea al waterfall."""
        if len(spectrum) != self.width:
            spectrum = np.interp(
                np.linspace(0, len(spectrum), self.width), np.arange(len(spectrum)), spectrum
            )
        self._data = np.roll(self._data, 1, axis=0)
        self._data[0, :] = spectrum
        self._index = (self._index + 1) % self.height

    def get_image(self) -> np.ndarray:
        """Retorna imagen del waterfall."""
        return self._data.copy()

    def clear(self) -> None:
        """Limpia waterfall."""
        self._data[:] = 0
        self._index = 0
