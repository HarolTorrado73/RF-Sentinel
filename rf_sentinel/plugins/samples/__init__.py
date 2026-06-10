"""Plugins de ejemplo para RF Sentinel."""

from .energy_detection import EnergyDetectionPlugin
from .template_detection import TemplateDetectionPlugin

__all__ = ["TemplateDetectionPlugin", "EnergyDetectionPlugin"]
