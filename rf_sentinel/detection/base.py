"""Detección de señales."""

from abc import ABC, abstractmethod

import numpy as np


class Detector(ABC):
    """Interfaz base para detectores de señales."""

    @abstractmethod
    def detect(
        self, data: np.ndarray, frequencies: np.ndarray | None = None
    ) -> list[dict[str, float]]:
        """Detecta señales en los datos.

        Retorna lista de detecciones con keys:
        - frequency: float (Hz)
        - power: float (dBm)
        - bandwidth: float (Hz)
        """
        pass
