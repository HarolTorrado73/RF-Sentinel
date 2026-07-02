"""Pipeline end-to-end para deteccion y clasificacion RF."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import numpy as np

from rf_sentinel.classification.base import Classifier
from rf_sentinel.core.events import EVENT_SIGNAL_DETECTED, EventBus
from rf_sentinel.detection.base import Detector


class DetectionPipeline:
    """Orquesta deteccion y clasificacion sobre muestras IQ."""

    def __init__(
        self,
        detector: Detector,
        classifier: Classifier,
        event_bus: EventBus | None = None,
    ) -> None:
        self.detector = detector
        self.classifier = classifier
        self.event_bus = event_bus

    def run(
        self,
        samples: np.ndarray,
        frequencies: np.ndarray | None = None,
    ) -> list[dict[str, Any]]:
        detections = self.detector.detect(samples, frequencies)
        results: list[dict[str, Any]] = []

        for detection in detections:
            classified = self.classifier.classify(detection)
            result: dict[str, Any] = {
                "frequency": float(detection.get("frequency", 0.0)),
                "bandwidth": float(detection.get("bandwidth", 0.0)),
                "power": float(detection.get("power", 0.0)),
                "modulation": classified.get("modulation"),
                "classification": classified.get("type"),
                "confidence": classified.get("confidence"),
                "timestamp": datetime.now(UTC),
            }
            results.append(result)

            if self.event_bus:
                self.event_bus.publish(EVENT_SIGNAL_DETECTED, result)

        return results