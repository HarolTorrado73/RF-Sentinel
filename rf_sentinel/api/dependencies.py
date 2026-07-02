"""Dependencias e inyección de la API."""

from rf_sentinel.classification.base import Classifier
from rf_sentinel.classification.rule_based import SignalClassifier
from rf_sentinel.core.events import EventBus
from rf_sentinel.detection.energy import EnergyDetector
from rf_sentinel.devices.mock import MockSDR
from rf_sentinel.devices.registry import DeviceRegistry
from rf_sentinel.services.capture_service import CaptureService
from rf_sentinel.services.export_service import ExportService
from rf_sentinel.services.pipeline import DetectionPipeline
from rf_sentinel.services.scan_service import ScanService


_scan_service = ScanService()
_capture_service = CaptureService()
_export_service = ExportService()
_detector = EnergyDetector()
_classifier: Classifier = SignalClassifier()
_event_bus = EventBus()
_pipeline = DetectionPipeline(_detector, _classifier, _event_bus)
_device_registry = DeviceRegistry()
_device_registry.register(MockSDR())


def get_scan_service() -> ScanService:
    return _scan_service


def get_capture_service() -> CaptureService:
    return _capture_service


def get_export_service() -> ExportService:
    return _export_service


def get_detector() -> EnergyDetector:
    return _detector


def get_classifier() -> SignalClassifier:
    return _classifier


def get_detection_pipeline() -> DetectionPipeline:
    return _pipeline


def get_device_registry() -> DeviceRegistry:
    return _device_registry
