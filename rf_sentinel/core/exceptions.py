"""Excepciones custom de RF Sentinel."""


class RFSError(Exception):
    """Error base de RF Sentinel."""
    pass


class DeviceError(RFSError):
    """Error de dispositivo SDR."""
    pass


class ScanError(RFSError):
    """Error de escaneo."""
    pass


class CaptureError(RFSError):
    """Error de captura."""
    pass


class ClassificationError(RFSError):
    """Error de clasificación."""
    pass
