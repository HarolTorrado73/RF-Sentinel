"""Dependencias e inyección de la API."""

from rf_sentinel.classification.rule_based import SignalClassifier
from rf_sentinel.detection.energy import EnergyDetector
from rf_sentinel.services.capture_service import CaptureService
from rf_sentinel.services.export_service import ExportService
from rf_sentinel.services.scan_service import ScanService


def get_scan_service() -> ScanService:
    return ScanService()


def get_capture_service() -> CaptureService:
    return CaptureService()


def get_export_service() -> ExportService:
    return ExportService()


def get_detector() -> EnergyDetector:
    return EnergyDetector()


def get_classifier() -> SignalClassifier:
    return SignalClassifier()
