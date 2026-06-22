"""RF Sentinel - Plataforma de análisis de radiofrecuencia."""

__version__ = "0.1.0"
__author__ = "RF Sentinel Team"

from rf_sentinel.analysis import Demodulator, SpectrumAnalyzer, Waterfall  # noqa: F401
from rf_sentinel.classification import Classifier, MLClassifier, SignalClassifier  # noqa: F401
from rf_sentinel.core import (  # noqa: F401
    CaptureDict,
    CaptureError,
    ClassificationError,
    DeviceError,
    EventBus,
    RFSError,
    ScanDict,
    ScanError,
    Settings,
    SignalDict,
    settings,
)
from rf_sentinel.database.models import Capture, Signal  # noqa: F401
from rf_sentinel.detection import Detector, EnergyDetector, PeakFinder, SignalDetector  # noqa: F401
from rf_sentinel.devices import HackRFSource, RTLSDRSource, SDRDevice  # noqa: F401
from rf_sentinel.services import CaptureService, ExportService, ScanService  # noqa: F401

__all__ = [
    "__version__",
    "Settings",
    "settings",
    "EventBus",
    "SignalDict",
    "CaptureDict",
    "ScanDict",
    "RFSError",
    "DeviceError",
    "ScanError",
    "CaptureError",
    "ClassificationError",
    "SDRDevice",
    "RTLSDRSource",
    "HackRFSource",
    "Capture",
    "Signal",
    "SpectrumAnalyzer",
    "Waterfall",
    "Demodulator",
    "Detector",
    "SignalDetector",
    "EnergyDetector",
    "PeakFinder",
    "Classifier",
    "SignalClassifier",
    "MLClassifier",
    "ScanService",
    "CaptureService",
    "ExportService",
]
