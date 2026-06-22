"""Routers de la API."""

from rf_sentinel.api.routers.captures import router as captures_router
from rf_sentinel.api.routers.classification import router as classification_router
from rf_sentinel.api.routers.detection import router as detection_router
from rf_sentinel.api.routers.export import router as export_router
from rf_sentinel.api.routers.scans import router as scans_router

__all__ = [
    "scans_router",
    "captures_router",
    "detection_router",
    "classification_router",
    "export_router",
]
