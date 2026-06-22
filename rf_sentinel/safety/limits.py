"""Límites regulatorios y de seguridad."""

# Límites de frecuencia por región (Hz)
FREQUENCY_LIMITS = {
    "US": (0, 6e9),
    "EU": (0, 6e9),
    "JP": (0, 6e9),
}

# Límites de potencia (dBm)
POWER_LIMITS = {
    "max_tx_power": 30.0,
    "max_eirp": 36.0,
}

# Bandas restringidas
RESTRICTED_BANDS = [
    (0.0, 9e3),       # VLF
    (135.7e3, 13.55e6),  # HF restringido
]


def check_frequency_limits(freq: float, region: str = "US") -> bool:
    """Verifica si una frecuencia está dentro de límites."""
    min_f, max_f = FREQUENCY_LIMITS.get(region, (0, 6e9))
    return min_f <= freq <= max_f


def check_power_limits(power: float) -> bool:
    """Verifica si una potencia está dentro de límites."""
    return power <= POWER_LIMITS["max_tx_power"]
