"""Detección de señales."""

from .detector import SignalDetector
from .energy_detector import EnergyDetector
from .peak_finder import PeakFinder

__all__ = ["SignalDetector", "PeakFinder", "EnergyDetector"]
