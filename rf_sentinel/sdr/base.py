"""Interfaz base para dispositivos SDR."""

from abc import ABC, abstractmethod


class SDRDevice(ABC):
    """Interfaz base para todos los dispositivos SDR."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre del dispositivo."""
        pass

    @property
    @abstractmethod
    def frequency_range(self) -> tuple[float, float]:
        """Rango de frecuencias soportado (min, max) en Hz."""
        pass

    @property
    @abstractmethod
    def sample_rates(self) -> list[float]:
        """Tasas de muestreo soportadas en Hz."""
        pass

    @abstractmethod
    def open(self) -> None:
        """Abre la conexión con el dispositivo."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Cierra la conexión con el dispositivo."""
        pass

    @abstractmethod
    def set_frequency(self, freq: float) -> None:
        """Configura la frecuencia central en Hz."""
        pass

    @abstractmethod
    def set_sample_rate(self, rate: float) -> None:
        """Configura la tasa de muestreo en Hz."""
        pass

    @abstractmethod
    def read_samples(self, num_samples: int) -> bytes:
        """Lee muestras IQ."""
        pass

    @property
    def is_open(self) -> bool:
        """Si el dispositivo está abierto."""
        return getattr(self, "_is_open", False)
