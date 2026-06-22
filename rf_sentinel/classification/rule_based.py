"""Clasificador de señales."""

from typing import Any

from rf_sentinel.classification.base import Classifier


class SignalClassifier(Classifier):
    """Clasificador básico de señales."""

    MODULATIONS = {
        "ask": {"bandwidth": (1e3, 100e3), "keywords": ["sensor", "remote"]},
        "fsk": {"bandwidth": (10e3, 500e3), "keywords": ["data", "telemetry"]},
        "ofdm": {"bandwidth": (1e6, 20e6), "keywords": ["wifi", "wifi-like"]},
        "am": {"bandwidth": (100e3, 200e3), "keywords": ["audio"]},
        "fm": {"bandwidth": (100e3, 250e3), "keywords": ["audio"]},
    }

    def classify(self, signal: dict[str, Any]) -> dict[str, Any]:
        """Clasifica una señal por características."""
        bandwidth = signal.get("bandwidth", 100e3)
        _ = signal.get("power", -60.0)

        best_match = "unknown"
        confidence = 0.0

        for mod, specs in self.MODULATIONS.items():
            min_bw, max_bw = specs["bandwidth"]
            if min_bw <= bandwidth <= max_bw:
                confidence = 0.7
                best_match = mod
                break

        return {
            "modulation": best_match,
            "confidence": confidence,
            "type": self._get_type(best_match),
        }

    def _get_type(self, modulation: str) -> str:
        types = {
            "ask": "Digital",
            "fsk": "Digital",
            "ofdm": "Digital",
            "am": "Analog",
            "fm": "Analog",
        }
        return types.get(modulation, "Unknown")
