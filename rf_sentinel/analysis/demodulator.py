"""Demodulación de señales."""

import numpy as np


class Demodulator:
    """Demodulador genérico."""

    def demodulate(self, samples: np.ndarray, modulation: str = "am") -> np.ndarray:
        """Demodula señal según tipo."""
        methods = {
            "am": self._am_demod,
            "fm": self._fm_demod,
            "ask": self._ask_demod,
            "fsk": self._fsk_demod,
        }
        method = methods.get(modulation, self._am_demod)
        return method(samples)

    def _am_demod(self, samples: np.ndarray) -> np.ndarray:
        """Demodulación AM."""
        return np.abs(samples)

    def _fm_demod(self, samples: np.ndarray) -> np.ndarray:
        """Demodulación FM."""
        return np.angle(samples[1:] * np.conj(samples[:-1]))

    def _ask_demod(self, samples: np.ndarray) -> np.ndarray:
        """Demodulación ASK."""
        envelope = np.abs(samples)
        return (envelope > np.mean(envelope)).astype(float)

    def _fsk_demod(self, samples: np.ndarray) -> np.ndarray:
        """Demodulación FSK real."""
        phase_diff = np.angle(samples[1:] * np.conj(samples[:-1]))
        return (phase_diff > 0).astype(float)
