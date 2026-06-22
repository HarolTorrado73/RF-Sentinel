"""Plugins builtin de RF Sentinel."""

from rf_sentinel.plugins.builtin.energy_detection import EnergyDetectionPlugin
from rf_sentinel.plugins.builtin.template_detection import TemplateDetectionPlugin

__all__ = ["EnergyDetectionPlugin", "TemplateDetectionPlugin"]
