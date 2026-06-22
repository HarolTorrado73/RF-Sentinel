"""Clasificación de señales."""

from abc import ABC, abstractmethod
from typing import Any


class Classifier(ABC):
    """Interfaz base para clasificadores de señales."""

    @abstractmethod
    def classify(self, signal: dict[str, Any]) -> dict[str, Any]:
        """Clasifica una señal.

        Retorna dict con keys:
        - modulation: str
        - confidence: float
        - type: str
        """
        pass
