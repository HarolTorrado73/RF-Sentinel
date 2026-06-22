"""Alias de compatibilidad: rf_sentinel.sdr → rf_sentinel.devices."""

from rf_sentinel.devices.base import SDRDevice  # noqa: F401
from rf_sentinel.devices.hackrf import HackRFSource  # noqa: F401
from rf_sentinel.devices.rtl_sdr import RTLSDRSource  # noqa: F401

__all__ = ["SDRDevice", "RTLSDRSource", "HackRFSource"]
