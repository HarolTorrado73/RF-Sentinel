"""Validadores de entrada."""

from rf_sentinel.core.exceptions import RFSError


def validate_frequency(freq: float) -> None:
    """Valida frecuencia en Hz."""
    if freq <= 0:
        raise RFSError(f"Frequency must be positive: {freq}")
    if freq > 10e9:
        raise RFSError(f"Frequency exceeds maximum: {freq}")


def validate_power(power: float) -> None:
    """Valida potencia en dBm."""
    if power > 30:
        raise RFSError(f"Power exceeds safety limit: {power} dBm")


def validate_sample_rate(rate: float) -> None:
    """Valida tasa de muestreo en Hz."""
    if rate <= 0:
        raise RFSError(f"Sample rate must be positive: {rate}")
