"""Detección de señales."""

from rf_sentinel.detection.base import Detector
from rf_sentinel.detection.energy import EnergyDetector
from rf_sentinel.detection.peak import PeakFinder
from rf_sentinel.detection.threshold import SignalDetector

__all__ = ["Detector", "SignalDetector", "EnergyDetector", "PeakFinder"]
