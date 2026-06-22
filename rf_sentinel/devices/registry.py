"""Registro y descubrimiento de dispositivos SDR."""

from typing import TYPE_CHECKING

from rf_sentinel.devices.base import SDRDevice

if TYPE_CHECKING:
    pass


class DeviceRegistry:
    """Registro central de dispositivos SDR disponibles."""

    def __init__(self) -> None:
        self._devices: dict[str, SDRDevice] = {}

    def register(self, device: SDRDevice) -> None:
        """Registra un dispositivo."""
        self._devices[device.name] = device

    def unregister(self, name: str) -> None:
        """Desregistra un dispositivo."""
        self._devices.pop(name, None)

    def get(self, name: str) -> SDRDevice | None:
        """Obtiene un dispositivo por nombre."""
        return self._devices.get(name)

    def list_devices(self) -> list[str]:
        """Lista nombres de dispositivos registrados."""
        return list(self._devices.keys())

    def get_default(self) -> SDRDevice | None:
        """Obtiene el primer dispositivo disponible."""
        return next(iter(self._devices.values()), None)
