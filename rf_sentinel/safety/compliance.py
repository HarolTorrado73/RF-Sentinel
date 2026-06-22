"""Cumplimiento regulatorio."""

from rf_sentinel.safety.limits import (
    RESTRICTED_BANDS,
    check_frequency_limits,
    check_power_limits,
)


class ComplianceChecker:
    """Verifica cumplimiento regulatorio."""

    def validate_tx(
        self, frequency: float, power: float, region: str = "US"
    ) -> tuple[bool, str]:
        """Valida transmisión contra límites regulatorios."""
        if not check_frequency_limits(frequency, region):
            return False, f"Frequency {frequency} out of limits for {region}"
        if not check_power_limits(power):
            return False, f"Power {power} exceeds maximum"
        return True, "OK"

    def is_restricted_band(self, frequency: float) -> bool:
        """Verifica si la frecuencia está en banda restringida."""
        return any(min_f <= frequency <= max_f for min_f, max_f in RESTRICTED_BANDS)
