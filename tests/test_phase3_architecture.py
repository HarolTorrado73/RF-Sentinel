import numpy as np

from rf_sentinel.api.dependencies import (
    get_capture_service,
    get_detection_pipeline,
    get_device_registry,
    get_scan_service,
)
from rf_sentinel.core.events import EVENT_SIGNAL_DETECTED, EventBus
from rf_sentinel.plugins import get_plugin, list_plugins
from rf_sentinel.plugins.core.loader import load_builtin_plugins
from rf_sentinel.services.pipeline import DetectionPipeline


def test_dependencies_are_singletons() -> None:
    scan_service_1 = get_scan_service()
    scan_service_2 = get_scan_service()
    capture_service_1 = get_capture_service()
    capture_service_2 = get_capture_service()

    assert scan_service_1 is scan_service_2
    assert capture_service_1 is capture_service_2


def test_device_registry_has_default_mock() -> None:
    registry = get_device_registry()
    devices = registry.list_devices()

    assert any(name.startswith("MockSDR") for name in devices)


def test_detection_pipeline_publishes_event() -> None:
    pipeline = get_detection_pipeline()
    event_bus = EventBus()

    captured: list[dict] = []
    event_bus.subscribe(EVENT_SIGNAL_DETECTED, captured.append)

    test_pipeline = DetectionPipeline(
        detector=pipeline.detector,
        classifier=pipeline.classifier,
        event_bus=event_bus,
    )

    samples = np.ones(2048, dtype=np.complex64)
    results = test_pipeline.run(samples)

    assert isinstance(results, list)
    assert len(captured) == len(results)


def test_plugin_loader_registers_builtin_plugins() -> None:
    load_builtin_plugins()
    names = list_plugins()

    assert "energy_detection" in names
    assert "template_detection" in names
    assert get_plugin("energy_detection") is not None


def test_sdr_backward_compatibility_alias() -> None:
    from rf_sentinel.sdr import RTLSDRSource  # noqa: PLC0415

    device = RTLSDRSource()
    assert device.name.startswith("RTL-SDR")
