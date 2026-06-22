# Plan de Migración FASE 3 - RF Sentinel

## Resumen Ejecutivo

Migrar de estructura monolítica a arquitectura modular en **11 pasos** secuenciales. Cada paso es independiente, testeable y con rollback posible. Duración estimada: 2-3 días de desarrollo.

---

## Paso 1: Crear `core/` (Base de la arquitectura)

**Objetivo:** Establecer el núcleo compartido sin dependencias externas.

**Archivos a crear:**
- `rf_sentinel/core/__init__.py`
- `rf_sentinel/core/config.py`
- `rf_sentinel/core/events.py`
- `rf_sentinel/core/types.py`
- `rf_sentinel/core/exceptions.py`

**Archivos afectados:** Ninguno (nuevos archivos)

**Cambios:**
1. `config.py` — Pydantic `BaseSettings` con valores de `.env`:
   - `DATABASE_URL`
   - `SDR_DEFAULT_DEVICE`
   - `API_HOST`, `API_PORT`
   - `LOG_LEVEL`
2. `events.py` — Event bus simple pub/sub:
   - `subscribe(event_name, callback)`
   - `publish(event_name, data)`
   - Eventos: `scan_started`, `scan_stopped`, `signal_detected`, `capture_created`
3. `types.py` — Tipos compartidos:
   - `SignalDict` (typing.TypedDict)
   - `CaptureDict`
   - `ScanDict`
   - `Frequency`, `Power`, `Bandwidth` (NewType)
4. `exceptions.py` — Jerarquía de excepciones:
   - `RFSError` (base)
   - `DeviceError`, `ScanError`, `CaptureError`, `ClassificationError`

**Validaciones:**
- `python -c "from rf_sentinel.core import config, events, types, exceptions"` — imports exitosos
- Tests unitarios de event bus (pub/sub)
- Tests de configuración (valores por defecto + override por env)

**Riesgo:** Bajo — no toca código existente

---

## Paso 2: Mover `devices/` desde `sdr/`

**Objetivo:** Renombrar paquete `sdr/` → `devices/` y agregar registry.

**Archivos a crear:**
- `rf_sentinel/devices/__init__.py`
- `rf_sentinel/devices/registry.py`
- `rf_sentinel/devices/mock.py`

**Archivos a mover:**
- `sdr/base.py` → `devices/base.py`
- `sdr/rtl_sdr.py` → `devices/rtl_sdr.py`
- `sdr/hackrf.py` → `devices/hackrf.py`

**Archivos a eliminar:**
- `sdr/__init__.py`

**Cambios:**
1. Mover archivos físicamente
2. Actualizar imports en `devices/rtl_sdr.py`: `from .base import SDRDevice`
3. Actualizar imports en `devices/hackrf.py`: `from .base import SDRDevice`
4. Crear `registry.py`:
   ```python
   class DeviceRegistry:
       def register(self, device: SDRDevice) -> None
       def get(self, name: str) -> SDRDevice | None
       def list_devices(self) -> list[str]
   ```
5. Crear `mock.py` — dispositivo mock para testing
6. Agregar alias temporal en `sdr/__init__.py` para backward compatibility:
   ```python
   from rf_sentinel.devices.base import SDRDevice
   ```

**Validaciones:**
- Todos los imports de `rf_sentinel.sdr.*` funcionan (via alias)
- Tests de devices pasan
- Registry lista dispositivos correctamente

**Riesgo:** Medio — rompe imports existentes. Mitigación: alias temporal + actualizar imports en misión siguiente.

---

## Paso 3: Separar `database/` en models + session + repositories

**Objetivo:** Separar responsabilidades en `database/`.

**Archivos a crear:**
- `rf_sentinel/database/models/__init__.py`
- `rf_sentinel/database/models/capture.py`
- `rf_sentinel/database/models/signal.py`
- `rf_sentinel/database/repositories/__init__.py`
- `rf_sentinel/database/repositories/capture_repo.py`
- `rf_sentinel/database/repositories/signal_repo.py`
- `rf_sentinel/database/session.py`

**Archivos a modificar:**
- `rf_sentinel/database/models.py` → mantener como legacy (re-exporta)

**Cambios:**
1. Extraer `Capture` y `Signal` a archivos separados en `models/`
2. Extraer engine/session a `session.py`
3. Crear `CaptureRepository` y `SignalRepository` con métodos CRUD async
4. `models.py` legacy re-exporta todo para compatibilidad

**Validaciones:**
- `Base.metadata.create_all()` funciona
- Repositorios pueden crear/leer/eliminar captures y signals
- `get_db()` sigue funcionando (via legacy `models.py`)

**Riesgo:** Bajo — código existente sigue funcionando via legacy imports

---

## Paso 4: Reestructurar `analysis/` (sin cambios mayores)

**Objetivo:** Preparar analysis para recibir mejoras futuras.

**Archivos a crear:**
- `rf_sentinel/analysis/__init__.py` (mejorar exports)

**Archivos a modificar:**
- `rf_sentinel/analysis/demodulator.py` — Corregir FSK:
  ```python
  def _fsk_demod(self, samples):
      # FSK real: comparar fase entre símbolos
      phase_diff = np.angle(samples[1:] * np.conj(samples[:-1]))
      return (phase_diff > 0).astype(float)
  ```

**Validaciones:**
- `SpectrumAnalyzer.analyze()` retorna psd_db + frequencies
- `Waterfall.add_spectrum()` funciona
- `Demodulator.demodulate("fsk", samples)` retorna resultado distinto a ASK

**Riesgo:** Bajo

---

## Paso 5: Renombrar y estructurar `detection/`

**Objetivo:** Limpiar nombres y agregar ABC.

**Archivos a crear:**
- `rf_sentinel/detection/base.py` — `Detector` ABC

**Archivos a renombrar:**
- `detector.py` → `threshold.py`
- `energy_detector.py` → `energy.py`
- `peak_finder.py` → `peak.py`

**Cambios:**
1. Crear `Detector` ABC con método `detect()` abstracto
2. Hacer que `SignalDetector`, `EnergyDetector`, `PeakFinder` implementen `Detector`
3. Actualizar imports en `plugins/builtin/energy_detection.py` (paso 9)

**Validaciones:**
- `isinstance(detector, Detector)` funciona para las 3 implementaciones
- Tests de detección pasan

**Riesgo:** Bajo — solo renombres + ABC

---

## Paso 6: Reestructurar `classification/`

**Objetivo:** Limpiar nombres y corregir bug en FeatureExtractor.

**Archivos a renombrar:**
- `classifier.py` → `rule_based.py`
- `ml_classifier.py` → `ml.py`

**Archivos a modificar:**
- `features.py` — Corregir `_estimate_bandwidth()`:
  ```python
  # Ahora retorna: float(np.sum(psd > threshold))  # índice de bin
  # Debe retornar: float en Hz
  fft = np.fft.fft(samples)
  psd = np.abs(fft) ** 2
  threshold = np.max(psd) * 0.1
  significant_bins = np.where(psd > threshold)[0]
  if len(significant_bins) == 0:
      return 0.0
  bin_width = self.sample_rate / len(samples)
  return float((significant_bins[-1] - significant_bins[0]) * bin_width)
  ```

**Validaciones:**
- `FeatureExtractor.extract()` retorna bandwidth en Hz, no en bins
- `SignalClassifier.classify()` funciona
- Tests pasan

**Riesgo:** Bajo

---

## Paso 7: Conectar `services/` a `database/`

**Objetivo:** Los servicios usan repositorios en lugar de in-memory.

**Archivos a modificar:**
- `rf_sentinel/services/scan_service.py`
- `rf_sentinel/services/capture_service.py`

**Cambios:**
1. `ScanService.__init__` recibe `CaptureRepository` (DI)
2. `ScanService.start_scan()` persiste en DB
3. `CaptureService.__init__` recibe `CaptureRepository` + `SignalRepository`
4. `CaptureService.create_capture()` guarda en DB
5. Mantener compatibilidad: si no se inyecta repo, usar in-memory (fallback)

**Validaciones:**
- `ScanService` puede crear y recuperar scans desde DB
- `CaptureService` puede crear captures y signals persistentes
- Tests con mock repositorios pasan

**Riesgo:** Medio — cambia comportamiento de services. Mitigación: fallback a in-memory.

---

## Paso 8: Reestructurar `plugins/`

**Objetivo:** Separar core de builtin, agregar loader.

**Archivos a crear:**
- `rf_sentinel/plugins/core/__init__.py`
- `rf_sentinel/plugins/core/loader.py`
- `rf_sentinel/plugins/builtin/__init__.py`

**Archivos a mover:**
- `plugins/__init__.py` → `plugins/core/base.py` (ABCs)
- `plugins/__init__.py` → `plugins/core/registry.py` (registry functions)
- `plugins/samples/energy_detection.py` → `plugins/builtin/energy_detection.py`
- `plugins/samples/template_detection.py` → `plugins/builtin/template_detection.py`

**Archivos a eliminar:**
- `plugins/samples/__init__.py` (si existe)

**Cambios:**
1. `plugins/core/base.py` — Solo ABCs (`PluginBase`, `DetectionPlugin`, etc.)
2. `plugins/core/registry.py` — Solo funciones de registry
3. `plugins/core/loader.py` — Auto-discovery de plugins en `builtin/`
4. `plugins/builtin/energy_detection.py` — Usar `detection.energy.EnergyDetector` como backend (eliminar duplicación)
5. Alias temporal en `plugins/__init__.py` para compatibilidad

**Validaciones:**
- `register_plugin()` sigue funcionando
- `list_plugins()` retorna plugins builtin
- Auto-discovery carga plugins automáticamente

**Riesgo:** Medio — plugins son parte de la extensibilidad. Mitigación: alias + tests.

---

## Paso 9: Reestructurar `api/` — Separar routers

**Objetivo:** Dividir `api/main.py` en routers + conectar services.

**Archivos a crear:**
- `rf_sentinel/api/routers/__init__.py`
- `rf_sentinel/api/routers/scans.py`
- `rf_sentinel/api/routers/captures.py`
- `rf_sentinel/api/routers/detection.py`
- `rf_sentinel/api/routers/classification.py`
- `rf_sentinel/api/routers/export.py`
- `rf_sentinel/api/dependencies.py`
- `rf_sentinel/api/schemas/` (mover Pydantic models)

**Archivos a modificar:**
- `rf_sentinel/api/main.py` — App factory que incluye routers

**Cambios:**
1. Extraer schemas Pydantic a `api/schemas/`
2. Extraer cada grupo de endpoints a su router
3. Crear `dependencies.py` con DI:
   ```python
   def get_scan_service() -> ScanService
   def get_capture_service() -> CaptureService
   def get_device_registry() -> DeviceRegistry
   ```
4. Reemplazar mocks por llamadas a services
5. Corregir CORS: reemplazar `allow_origins=["*"]` por env variable

**Validaciones:**
- Todos los endpoints responden correctamente
- `POST /scan` usa `ScanService.start_scan()`
- `POST /detect` usa `DetectionPipeline`
- OpenAPI docs generadas automáticamente

**Riesgo:** Alto — API es la cara del sistema. Mitigación: tests de endpoints + rollback rápido.

---

## Paso 10: Conectar `ui/desktop/` a services

**Objetivo:** UI deja de usar mock data, consume services.

**Archivos a modificar:**
- `rf_sentinel/ui/desktop/main.py`

**Cambios:**
1. `RFMainUI.__init__` recibe `ScanService` y `DeviceRegistry` (DI)
2. `_update_display()` obtiene datos de `ScanService` en lugar de `np.random`
3. Botón "Escanear" llama a `ScanService.start_scan()`
4. `WaterfallWidget` consume `Waterfall` de analysis/
5. Agregar conexión a dispositivo SDR real

**Validaciones:**
- UI muestra datos reales del backend
- Escaneo inicia/para correctamente
- Waterfall actualiza con datos reales

**Riesgo:** Medio — UI es crítica para usuarios desktop. Mitigación: mantener fallback a mock si no hay device.

---

## Paso 11: Crear módulos nuevos (`safety/`, `config/`, `utils/`)

**Objetivo:** Completar arquitectura con módulos de soporte.

**Archivos a crear:**
- `rf_sentinel/safety/__init__.py`
- `rf_sentinel/safety/limits.py`
- `rf_sentinel/safety/compliance.py`
- `rf_sentinel/safety/watchdog.py`
- `rf_sentinel/config/__init__.py`
- `rf_sentinel/config/settings.py`
- `rf_sentinel/config/defaults.py`
- `rf_sentinel/utils/__init__.py`
- `rf_sentinel/utils/logging.py`
- `rf_sentinel/utils/validators.py`
- `rf_sentinel/utils/conversions.py`

**Cambios:**
1. Mover constantes de límites de frecuencia/power a `safety/limits.py`
2. Configuración centralizada en `config/settings.py`
3. Logging estructurado en `utils/logging.py`

**Validaciones:**
- `rf_sentinel config` muestra configuración cargada
- Límites de frecuencia se aplican antes de transmitir
- Logs usan formato estructurado

**Riesgo:** Bajo — módulos nuevos, sin impacto en existente

---

## Checklist de Validación Global

| Check | Comando | Esperado |
|-------|---------|----------|
| Imports | `python -c "import rf_sentinel"` | Sin errores |
| Tests unitarios | `pytest tests/` | Todos pasan |
| Lint | `ruff check rf_sentinel/` | Sin errores |
| API arranca | `rf-sentinel api` | Servidor en puerto 8000 |
| UI arranca | `rf-sentinel ui` | Ventana Qt |
| DB init | `python -c "from rf_sentinel.database.session import init_db; init_db()"` | Crea `rf_sentinel.db` |
| Plugins | `python -c "from rf_sentinel.plugins.core.registry import list_plugins; print(list_plugins())"` | Lista plugins builtin |
| Devices | `python -c "from rf_sentinel.devices.registry import DeviceRegistry; print(DeviceRegistry().list_devices())"` | Lista RTL-SDR, HackRF, Mock |

---

## Timeline

| Día | Pasos | Entregable |
|-----|-------|------------|
| 1 | 1-3 | `core/`, `devices/`, `database/` reorganizados |
| 2 | 4-6 | `analysis/` corregido, `detection/` y `classification/` renombrados |
| 3 | 7-9 | `services/` conectados, `plugins/` reestructurado, `api/` con routers |
| 4 | 10-11 | UI conectada, `safety/` + `config/` + `utils/` creados |
| 5 | Validación | Tests + lint + deploy |

---

## Rollback Strategy

Cada paso tiene su propio rollback:
1. **Pasos 1-3:** No afectan código existente (solo crean/renombran)
2. **Pasos 4-6:** Solo renombres + correcciones menores
3. **Paso 7:** Mantener fallback a in-memory si DB falla
4. **Paso 8:** Alias en `plugins/__init__.py` mantienen compatibilidad
5. **Paso 9:** Rollback a `api/main.py` monolítico en 1 commit
6. **Paso 10:** Flag `USE_MOCK_DATA=true` para fallback
7. **Paso 11:** Módulos nuevos, no afectan existente
