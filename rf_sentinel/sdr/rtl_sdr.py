"""Implementación para RTL-SDR."""

from .base import SDRDevice


class RTLSDRSource(SDRDevice):
    """Interfaz para RTL-SDR."""

    def __init__(self, device_index: int = 0):
        self._device_index = device_index
        self._frequency = 0.0
        self._sample_rate = 2.4e6
        self._is_open = False

    @property
    def name(self) -> str:
        return f"RTL-SDR (device {self._device_index})"

    @property
    def frequency_range(self) -> tuple[float, float]:
        return (24.0e6, 1.7e9)

    @property
    def sample_rates(self) -> list[float]:
        return [2.4e6, 2.88e6, 3.2e6, 4.32e6]

    def open(self) -> None:
        self._is_open = True

    def close(self) -> None:
        self._is_open = False

    def set_frequency(self, freq: float) -> None:
        if not (self.frequency_range[0] <= freq <= self.frequency_range[1]):
            raise ValueError(f"Frequency {freq} out of range")
        self._frequency = freq

    def set_sample_rate(self, rate: float) -> None:
        if rate not in self.sample_rates:
            rate = min(self.sample_rates, key=lambda x: abs(x - rate))
        self._sample_rate = rate

    def read_samples(self, num_samples: int) -> bytes:
        if not self._is_open:
            raise RuntimeError("Device not open")
        # Mock data - real implementation uses librtlsdr
        return b"\x00" * (num_samples * 2)
