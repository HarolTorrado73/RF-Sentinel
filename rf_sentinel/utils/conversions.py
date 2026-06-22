"""Conversiones de unidades."""

import math


def hz_to_mhz(hz: float) -> float:
    """Convierte Hz a MHz."""
    return hz / 1e6


def mhz_to_hz(mhz: float) -> float:
    """Convierte MHz a Hz."""
    return mhz * 1e6


def dbm_to_watt(dbm: float) -> float:
    """Convierte dBm a vatios."""
    return 10 ** ((dbm - 30) / 10)


def watt_to_dbm(watt: float) -> float:
    """Convierte vatios a dBm."""
    if watt <= 0:
        return 0.0
    return 10 * math.log10(watt * 1000)
