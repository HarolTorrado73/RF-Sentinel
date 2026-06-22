# Interfaces FASE 3 - RF Sentinel

## 1. Visión General

Este documento define las **interfaces públicas** entre módulos. Cada interfaz es un contrato estricto: un módulo puede cambiar su implementación interna siempre que respete la interfaz pública.

**Principio:** Depender de abstracciones, no de implementaciones concretas.

---

## 2. Core Interfaces

### 2.1 `core/config.py` — Settings

```python
class Settings:
    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    SDR_DEFAULT_DEVICE: str = "mock"
    CORS_ALLOW_ORIGINS: list[str] = []
    ENABLE_PLUGINS: bool = True

    @classmethod
    def from_env(cls) -> "Settings"
```

**Consumidores:** Todos los módulos

---

### 2.2 `core/events.py` — Event Bus

```python
class EventBus:
    def subscribe(self, event_name: str, callback: Callable) -> None
    def unsubscribe(self, event_name: str, callback: Callable) -> None
    def publish(self, event_name: str, data: dict) -> None

# Eventos estándar
EVENT_SCAN_STARTED = "scan.started"
EVENT_SCAN_STOPPED = "scan.stopped"
EVENT_SCAN_PROGRESS = "scan.progress"
EVENT_SIGNAL_DETECTED = "signal.detected"
EVENT_CAPTURE_CREATED = "capture.created"
EVENT_CAPTURE_EXPORTED = "capture.exported"
EVENT_DEVICE_CONNECTED = "device.connected"
EVENT_DEVICE_DISCONNECTED = "device.disconnected"
```

**Consumidores:** Services, API (WebSocket), UI

---

### 2.3 `core/types.py` — Tipos Compartidos

```python
from typing import TypedDict
from datetime import datetime

class SignalDict(TypedDict):
    frequency: float      # Hz
    bandwidth: float      # Hz
    power: float          # dBm
    modulation: str | None
    classification: str | None
    confidence: float | None
    timestamp: datetime

class CaptureDict(TypedDict):
    id: int
    timestamp: datetime
    center_frequency: float
    sample_rate: float
    bandwidth: float | None
    duration: float
    filename: str | None
    peak_power: float | None
    noise_floor: float | None
    signals: list[SignalDict]

class ScanDict(TypedDict):
    scan_id: str
    status: str           # "running" | "completed" | "stopped" | "error"
    progress: float       # 0.0 to 100.0
    start_freq: float
    stop_freq: float
    step: float
    signals_detected: int
```

**Consumidores:** Todos los módulos

---

## 3. Devices Interfaces

### 3.1 `devices/base.py` — SDRDevice (ABC)

```python
from abc import ABC, abstractmethod

class SDRDevice(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def frequency_range(self) -> tuple[float, float]: ...  # (min_hz, max_hz)

    @property
    @abstractmethod
    def sample_rates(self) -> list[float]: ...

    @property
    def is_open(self) -> bool: ...

    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def set_frequency(self, freq: float) -> None: ...  # Hz

    @abstractmethod
    def set_sample_rate(self, rate: float) -> None: ...  # Hz

    @abstractmethod
    def read_samples(self, num_samples: int) -> bytes: ...  # I/Q interleaved
```

**Implementaciones:**
- `devices/rtl_sdr.py` — `RTLSDRSource(SDRDevice)`
- `devices/hackrf.py` — `HackRFSource(SDRDevice)`
- `devices/mock.py` — `MockSDR(SDRDevice)`

**Consumidores:** Services (ScanService, CaptureService), UI

---

### 3.2 `devices/registry.py` — DeviceRegistry

```python
class DeviceRegistry:
    def __init__(self) -> None
    def register(self, device: SDRDevice) -> None
    def unregister(self, name: str) -> None
    def get(self, name: str) -> SDRDevice | None
    def list_devices(self) -> list[str]
    def get_default(self) -> SDRDevice
```

**Consumidores:** Services, API, UI

---

## 4. Analysis Interfaces

### 4.1 `analysis/spectrum.py` — SpectrumAnalyzer

```python
class SpectrumAnalyzer:
    def __init__(self, sample_rate: float = 10e6, fft_size: int = 1024) -> None

    def analyze(self, samples: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Retorna (psd_db, frequencies_hz)."""

    def detect_peaks(self, spectrum: np.ndarray,
                     threshold: float = -60.0,
                     min_distance: int = 10) -> list[int]:
        """Retorna índices de picos."""
```

**Consumidores:** Detection (PeakFinder), UI, API

---

### 4.2 `analysis/waterfall.py` — Waterfall

```python
class Waterfall:
    def __init__(self, width: int = 1024, height: int = 256) -> None

    def add_spectrum(self, spectrum: np.ndarray) -> None
    def get_image(self) -> np.ndarray
    def clear(self) -> None
```

**Consumidores:** UI, API

---

### 4.3 `analysis/demodulator.py` — Demodulator

```python
class Demodulator:
    def demodulate(self, samples: np.ndarray, modulation: str = "am") -> np.ndarray:
        """Demodula según tipo: am, fm, ask, fsk."""

    def _am_demod(self, samples: np.ndarray) -> np.ndarray
    def _fm_demod(self, samples: np.ndarray) -> np.ndarray
    def _ask_demod(self, samples: np.ndarray) -> np.ndarray
    def _fsk_demod(self, samples: np.ndarray) -> np.ndarray  # FSK real (no ASK)
```

**Consumidores:** Classification, Services, UI

---

## 5. Detection Interfaces

### 5.1 `detection/base.py` — Detector (ABC)

```python
from abc import ABC, abstractmethod

class Detector(ABC):
    @abstractmethod
    def detect(self, data: np.ndarray,
               frequencies: np.ndarray | None = None) -> list[dict[str, float]]:
        """Retorna lista de detecciones con keys: frequency, power, bandwidth."""
```

**Implementaciones:**
- `detection/threshold.py` — `SignalDetector(Detector)`
- `detection/energy.py` — `EnergyDetector(Detector)`
- `detection/peak.py` — `PeakFinder(Detector)`

**Consumidores:** Services (Pipeline), Classification, Plugins

---

## 6. Classification Interfaces

### 6.1 `classification/base.py` — Classifier (ABC)

```python
from abc import ABC, abstractmethod

class Classifier(ABC):
    @abstractmethod
    def classify(self, signal: SignalDict) -> dict[str, Any]:
        """Retorna {modulation, confidence, type}."""
```

**Implementaciones:**
- `classification/rule_based.py` — `SignalClassifier(Classifier)`
- `classification/ml.py` — `MLClassifier(Classifier)`

**Consumidores:** Services, API

---

### 6.2 `classification/features.py` — FeatureExtractor

```python
class FeatureExtractor:
    def __init__(self, sample_rate: float) -> None

    def extract(self, samples: np.ndarray) -> dict[str, Any]:
        """Retorna features: mean_power, std_power, peak_power,
        bandwidth (Hz), spectral_flatness, center_frequency."""
```

**Consumidores:** MLClassifier, Classification plugins

---

## 7. Database Interfaces

### 7.1 `database/models/capture.py` — Capture (SQLAlchemy)

```python
class Capture(Base):
    __tablename__ = "captures"
    id: int
    timestamp: datetime
    center_frequency: float
    sample_rate: float
    bandwidth: float | None
    duration: float
    filename: str | None
    peak_power: float | None
    noise_floor: float | None
    data: bytes | None
```

### 7.2 `database/models/signal.py` — Signal (SQLAlchemy)

```python
class Signal(Base):
    __tablename__ = "signals"
    id: int
    capture_id: int
    frequency: float
    bandwidth: float
    power: float
    modulation: str | None
    classification: str | None
    confidence: float | None
    timestamp: datetime
```

### 7.3 `database/repositories/capture_repo.py` — CaptureRepository

```python
class CaptureRepository:
    async def create(self, capture: Capture) -> Capture
    async def get(self, capture_id: int) -> Capture | None
    async def list(self, limit: int = 100, offset: int = 0) -> list[Capture]
    async def delete(self, capture_id: int) -> bool
```

### 7.4 `database/repositories/signal_repo.py` — SignalRepository

```python
class SignalRepository:
    async def create(self, signal: Signal) -> Signal
    async def get_by_capture(self, capture_id: int) -> list[Signal]
    async def get(self, signal_id: int) -> Signal | None
    async def delete(self, signal_id: int) -> bool
```

**Consumidores:** Services, API

---

## 8. Services Interfaces

### 8.1 `services/scan_service.py` — ScanService

```python
class ScanService:
    def __init__(self, device_registry: DeviceRegistry,
                 event_bus: EventBus) -> None

    async def start_scan(self, start_freq: float, stop_freq: float,
                         step: float = 1e6) -> str:
        """Inicia escaneo. Retorna scan_id."""

    async def get_status(self, scan_id: str) -> ScanDict
    async def stop_scan(self, scan_id: str) -> None
```

**Dependencias:** `DeviceRegistry`, `EventBus`

---

### 8.2 `services/capture_service.py` — CaptureService

```python
class CaptureService:
    def __init__(self, capture_repo: CaptureRepository,
                 signal_repo: SignalRepository,
                 event_bus: EventBus) -> None

    async def create_capture(self, frequency: float, duration: float,
                             sample_rate: float = 10e6) -> CaptureDict
    async def get_capture(self, capture_id: int) -> CaptureDict | None
    async def list_captures(self, limit: int = 100) -> list[CaptureDict]
    async def delete_capture(self, capture_id: int) -> bool
```

**Dependencias:** `CaptureRepository`, `SignalRepository`, `EventBus`

---

### 8.3 `services/export_service.py` — ExportService

```python
class ExportService:
    def export_to_json(self, data: CaptureDict) -> str
    def export_to_pdf(self, capture: CaptureDict) -> bytes
    def generate_filename(self, prefix: str, extension: str) -> str
```

**Dependencias:** Ninguna (standalone)

---

### 8.4 `services/pipeline.py` — Pipeline (nuevo)

```python
class Pipeline:
    def __init__(self, device: SDRDevice,
                 spectrum_analyzer: SpectrumAnalyzer,
                 detector: Detector,
                 classifier: Classifier,
                 capture_service: CaptureService) -> None

    async def run_scan(self, start_freq: float, stop_freq: float,
                       step: float = 1e6) -> ScanDict:
        """Ejecuta pipeline completo: SDR → FFT → Detección → Clasificación → DB."""

    async def stop(self) -> None
```

**Dependencias:** `SDRDevice`, `SpectrumAnalyzer`, `Detector`, `Classifier`, `CaptureService`

**Consumidores:** API, UI

---

## 9. Plugin Interfaces

### 9.1 `plugins/core/base.py` — PluginBase (ABC)

```python
class PluginBase(ABC):
    name: str
    version: str
    description: str
    priority: int

    @abstractmethod
    async def initialize(self) -> None: ...
    @abstractmethod
    async def cleanup(self) -> None: ...
    @abstractmethod
    def process(self, data: dict[str, Any]) -> dict[str, Any]: ...
```

### 9.2 `plugins/core/base.py` — DetectionPlugin

```python
class DetectionPlugin(PluginBase):
    name = "detection_base"

    @abstractmethod
    def detect(self, samples: bytes) -> list[dict[str, Any]]: ...
```

### 9.3 `plugins/core/base.py` — ClassificationPlugin

```python
class ClassificationPlugin(PluginBase):
    name = "classification_base"

    @abstractmethod
    def classify(self, signal: SignalDict) -> dict[str, Any]: ...
```

### 9.4 `plugins/core/base.py` — ExportPlugin

```python
class ExportPlugin(PluginBase):
    name = "export_base"

    @abstractmethod
    def export(self, capture: CaptureDict, format: str) -> bytes: ...
```

### 9.5 `plugins/core/registry.py` — PluginRegistry

```python
_plugins: dict[str, type[PluginBase]] = {}

def register_plugin(name: str, plugin_class: type[PluginBase]) -> None
def get_plugin(name: str) -> type[PluginBase] | None
def list_plugins() -> list[str]
def load_builtin_plugins() -> None
```

**Consumidores:** Services (Pipeline), API

---

## 10. API Interfaces

### 10.1 `api/routers/scans.py`

```python
@router.post("/scan", response_model=ScanResponse)
async def start_scan(request: ScanRequest,
                     scan_service: ScanService) -> ScanResponse

@router.get("/scan/{scan_id}", response_model=ScanResponse)
async def get_scan(scan_id: str,
                   scan_service: ScanService) -> ScanResponse

@router.post("/scan/{scan_id}/stop")
async def stop_scan(scan_id: str,
                    scan_service: ScanService) -> dict
```

### 10.2 `api/routers/captures.py`

```python
@router.get("/capture", response_model=list[CaptureResponse])
async def list_captures(capture_service: CaptureService,
                        limit: int = 100) -> list[CaptureResponse]

@router.get("/capture/{capture_id}", response_model=CaptureResponse)
async def get_capture(capture_id: int,
                      capture_service: CaptureService) -> CaptureResponse

@router.post("/capture", response_model=CaptureResponse)
async def create_capture(frequency: float, duration: float,
                         capture_service: CaptureService) -> CaptureResponse
```

### 10.3 `api/routers/detection.py`

```python
@router.post("/detect", response_model=list[SignalResponse])
async def detect_signals(capture_id: int,
                         detector: Detector) -> list[SignalResponse]
```

### 10.4 `api/routers/export.py`

```python
@router.post("/export/pdf")
async def export_pdf(capture_id: int,
                     export_service: ExportService) -> dict

@router.post("/export/json")
async def export_json(capture_id: int,
                      export_service: ExportService) -> dict
```

---

## 11. UI Interfaces

### 11.1 `ui/desktop/main.py` — RFMainUI

```python
class RFMainUI(QMainWindow):
    def __init__(self, scan_service: ScanService,
                 capture_service: CaptureService,
                 device_registry: DeviceRegistry) -> None
    # Widgets:
    # - SpectrumWidget: muestra datos de SpectrumAnalyzer
    # - WaterfallWidget: muestra datos de Waterfall
    # - Controles: frecuencia, dispositivo, escanear
```

**Consumidores:** Usuario desktop

---

## 12. Flujo de Datos Completo (Contratos)

```
Usuario → UI → ScanService → DeviceRegistry → SDRDevice.read_samples()
                                                    ↓
                                              SpectrumAnalyzer.analyze()
                                                    ↓
                                              Detector.detect()
                                                    ↓
                                              Classifier.classify()
                                                    ↓
                                              CaptureService.create_capture()
                                                    ↓
                                              SignalRepository.create()
                                                    ↓
                                              API retorna CaptureResponse
                                                    ↓
                                              ExportService.export_to_pdf()
```

Cada flecha es una llamada a una interfaz pública. El módulo downstream no conoce la implementación concreta del upstream, solo la interfaz.

---

## 13. Matriz de Dependencias

| Módulo | Depende de |
|--------|-----------|
| `core/` | stdlib only |
| `devices/` | `core/types`, `core/exceptions` |
| `analysis/` | `core/types`, numpy |
| `detection/` | `core/types`, `analysis/`, numpy |
| `classification/` | `core/types`, `detection/`, numpy/sklearn |
| `database/` | `core/types`, SQLAlchemy |
| `services/` | `core/events`, `devices/`, `analysis/`, `detection/`, `classification/`, `database/` |
| `plugins/core/` | `core/types`, `detection/`, `classification/` |
| `plugins/builtin/` | `plugins/core/`, `detection/`, `classification/` |
| `api/` | `core/config`, `services/`, `plugins/core/` |
| `ui/` | `core/config`, `services/` o `api/` |
| `safety/` | `devices/`, `core/config` |
| `config/` | `core/types` |
| `utils/` | stdlib only |

**Regla de oro:** Un módulo nunca importa de un módulo que está "arriba" en la cadena de valor.

---

## 14. Garantías de Compatibilidad

| Cambio Permitido | Sin Cambio de Interfaz |
|------------------|------------------------|
| Refactor interno de una clase | ✅ |
| Optimización de algoritmo | ✅ |
| Agregar métodos privados (`_method`) | ✅ |
| Agregar parámetros con default | ✅ |
| Cambiar excepciones internas | ✅ |
| Cambiar framework de DB (SQLAlchemy → Tortoise) | ✅ (si repositorios respetan interfaz) |

| Cambio que Requiere Actualización de Interfaz |
|----------------------------------------------|
| Agregar parámetro obligatorio a método público | ❌ |
| Cambiar tipo de retorno de método público | ❌ |
| Eliminar método público | ❌ |
| Cambiar nombre de clase ABC | ❌ |
| Cambiar firma de `detect()` en `Detector` | ❌ |
