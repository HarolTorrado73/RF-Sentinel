"""Interfaz gráfica principal."""

import sys
from typing import TYPE_CHECKING

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from rf_sentinel.devices.registry import DeviceRegistry
    from rf_sentinel.services.scan_service import ScanService


class SpectrumWidget(pg.GraphicsLayoutWidget):
    """Widget de espectro en tiempo real."""

    def __init__(self):
        super().__init__()
        self.plot = self.addPlot(title="Espectro en Tiempo Real")
        self.plot.setLabel("left", "Potencia", unit="dBm")
        self.plot.setLabel("bottom", "Frecuencia", unit="MHz")
        self.curve = self.plot.plot(pen="y")
        self.setYRange(-100, 0)

    def update_data(self, data: np.ndarray, frequencies: np.ndarray) -> None:
        self.curve.setData(frequencies / 1e6, data)


class WaterfallWidget(pg.GraphicsLayoutWidget):
    """Widget de waterfall."""

    def __init__(self):
        super().__init__()
        self.image = self.addPlot(title="Waterfall")
        self.img = pg.ImageItem()
        self.image.addItem(self.img)
        self.image.setLabel("left", "Tiempo")
        self.image.setLabel("bottom", "Frecuencia", unit="MHz")


class RFMainUI(QMainWindow):
    """Ventana principal de RF Sentinel."""

    def __init__(
        self,
        scan_service: "ScanService | None" = None,
        device_registry: "DeviceRegistry | None" = None,
    ):
        super().__init__()
        self.scan_service = scan_service
        self.device_registry = device_registry
        self.setWindowTitle("RF Sentinel - Spectrum Analyzer")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Spectrum display
        layout.addWidget(QLabel("<h2>Spectrum Analyzer</h2>"))
        self.spectrum = SpectrumWidget()
        layout.addWidget(self.spectrum)

        # Waterfall display
        layout.addWidget(QLabel("<h2>Waterfall</h2>"))
        self.waterfall = WaterfallWidget()
        layout.addWidget(self.waterfall)

        # Controls
        controls = QHBoxLayout()
        controls.addWidget(QLabel("Frecuencia:"))
        self.freq_slider = QSlider()
        self.freq_slider.setRange(0, 6000)
        controls.addWidget(self.freq_slider)

        controls.addWidget(QLabel("Dispositivo:"))
        self.device_combo = QComboBox()
        if self.device_registry:
            self.device_combo.addItems(self.device_registry.list_devices())
        else:
            self.device_combo.addItems(["HackRF One", "RTL-SDR"])
        controls.addWidget(self.device_combo)

        self.scan_btn = QPushButton("Escanear")
        controls.addWidget(self.scan_btn)

        auto_btn = QPushButton("Auto Scan")
        controls.addWidget(auto_btn)

        layout.addLayout(controls)

        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_display)
        self.timer.start(100)  # 10 FPS

    def _update_display(self) -> None:
        frequencies = np.linspace(100, 1000, 1000)
        spectrum_data = -60 + 20 * np.random.rand(1000)
        self.spectrum.update_data(spectrum_data, frequencies)


def main() -> None:
    app = QApplication(sys.argv)
    window = RFMainUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
