# Arquitectura FASE 3 - RF Sentinel

## 1. Estructura Propuesta

```
rf_sentinel/
├── __init__.py
├── main.py                          # CLI entry point (sin cambios)
│
├── api/                             # API REST
│   ├── __init__.py
│   ├── main.py                      # FastAPI app factory
│   ├── dependencies.py              # DI container / dependencias
│   └── routers/
│       ├── __init__.py
│       ├── scans.py                 # /scan endpoints
│       ├── captures.py              # /capture endpoints
│       ├── detection.py             # /detect endpoints
│       ├── classification.py        # /classify endpoints
│       └── export.py                # /export endpoints
│
├── core/                            # Abstracciones compartidas
│   ├── __init__.py
│   ├── config.py                    # Settings (Pydantic BaseSettings)
│   ├── events.py                    # Event bus interno
│   ├── types.py                     # Tipos compartidos (Signal, Capture, Scan)
│   └── exceptions.py                # Excepciones custom
│
├── devices/                         # Abstracción de hardware SDR
│   ├── __init__.py
│   ├── base.py                      # SDRDevice ABC (desde sdr/base.py)
│   ├── registry.py                  # Device discovery & registry
│   ├── rtl_sdr.py                   # RTL-SDR (desde sdr/rtl_sdr.py)
│   ├── hackrf.py                    # HackRF (desde sdr/hackrf.py)
│   └── mock.py                      # Mock device para testing
│
├── analysis/                        # Procesamiento de señal
│   ├── __init__.py
│   ├── spectrum.py                  # FFT SpectrumAnalyzer (mantener)
│   ├── waterfall.py                 # Waterfall buffer (mantener)
│   ├── demodulator.py               # Demodulación AM/FM/ASK/FSK (mantener, corregir FSK)
│   └── filters.py                   # Filtros FIR/IIR (nuevo, futuro)
│
├── detection/                       # Detección de señales
│   ├── __init__.py
│   ├── base.py                      # Detector ABC
│   ├── threshold.py                 # SignalDetector (desde detector.py)
│   ├── energy.py                    # EnergyDetector (desde energy_detector.py)
│   └── peak.py                      # PeakFinder (desde peak_finder.py)
│
├── classification/                  # Clasificación de señales
│   ├── __init__.py
│   ├── base.py                      # Classifier ABC
│   ├── rule_based.py                # SignalClassifier (desde classifier.py)
│   ├── ml.py                        # MLClassifier (desde ml_classifier.py)
│   └── features.py                  # FeatureExtractor (mantener, corregir bandwidth)
│
├── database/                        # Persistencia
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── capture.py               # Modelo Capture (desde models.py)
│   │   └── signal.py                # Modelo Signal (desde models.py)
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── capture_repo.py          # CRUD Capture (nuevo)
│   │   └── signal_repo.py           # CRUD Signal (nuevo)
│   └── session.py                   # Engine + session (desde models.py)
│
├── services/                        # Lógica de negocio
│   ├── __init__.py
│   ├── scan_service.py              # ScanService (mantener, conectar a DB)
│   ├── capture_service.py           # CaptureService (mantener, conectar a DB)
│   ├── export_service.py            # ExportService (mantener, lazy load)
│   └── pipeline.py                  # Pipeline RF end-to-end (nuevo)
│
├── ui/                              # Interfaces de usuario
│   ├── __init__.py
│   ├── desktop/
│   │   ├── __init__.py
│   │   └── main.py                  # Qt UI (mantener, conectar a services)
│   └── web/                         # Futuro UI web
│       └── app.py
│
├── safety/                          # Seguridad y límites
│   ├── __init__.py
│   ├── limits.py                    # Límites freq/power por región
│   ├── compliance.py                # Cumplimiento regulatorio
│   └── watchdog.py                  # Emergency stop
│
├── config/                          # Configuración
│   ├── __init__.py
│   ├── settings.py                  # Pydantic Settings
│   └── defaults.py                  # Valores por defecto
│
├── plugins/                         # Sistema de plugins
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base.py                  # PluginBase (desde plugins/__init__.py)
│   │   ├── registry.py              # Registry (desde plugins/__init__.py)
│   │   └── loader.py                # Auto-discovery loader (nuevo)
│   └── builtin/
│       ├── __init__.py
│       ├── energy_detection.py      # (corregir duplicación con detection/)
│       └── template_detection.py    # (mantener)
│
└── utils/                           # Utilidades
    ├── __init__.py
    ├── logging.py                   # Logging setup
    ├── validators.py                # Validación de entrada
    └── conversions.py               # Conversión de unidades
```

---

## 2. Mapeo de Archivos Actuales → Destino

| Archivo Actual | Destino | Acción | Notas |
|---------------|---------|--------|-------|
| `rf_sentinel/__init__.py` | `rf_sentinel/__init__.py` | Sin cambios | |
| `rf_sentinel/main.py` | `rf_sentinel/main.py` | Sin cambios | Entry point CLI |
| `rf_sentinel/api/main.py` | `rf_sentinel/api/main.py` + `routers/*.py` | Dividir | Extraer endpoints a routers |
| `rf_sentinel/database/models.py` | `rf_sentinel/database/models/` + `session.py` | Dividir | Separar modelos de engine |
| `rf_sentinel/services/scan_service.py` | `rf_sentinel/services/scan_service.py` | Mover | Conectar a DB |
| `rf_sentinel/services/capture_service.py` | `rf_sentinel/services/capture_service.py` | Mover | Conectar a DB |
| `rf_sentinel/services/export_service.py` | `rf_sentinel/services/export_service.py` | Mover | Lazy load reportlab |
| `rf_sentinel/sdr/base.py` | `rf_sentinel/devices/base.py` | Mover | |
| `rf_sentinel/sdr/rtl_sdr.py` | `rf_sentinel/devices/rtl_sdr.py` | Mover | |
| `rf_sentinel/sdr/hackrf.py` | `rf_sentinel/devices/hackrf.py` | Mover | Implementar set_gain/bandwidth |
| `rf_sentinel/analysis/spectrum.py` | `rf_sentinel/analysis/spectrum.py` | Sin cambios | |
| `rf_sentinel/analysis/waterfall.py` | `rf_sentinel/analysis/waterfall.py` | Sin cambios | |
| `rf_sentinel/analysis/demodulator.py` | `rf_sentinel/analysis/demodulator.py` | Corregir | FSK delega a ASK |
| `rf_sentinel/detection/detector.py` | `rf_sentinel/detection/threshold.py` | Renombrar | |
| `rf_sentinel/detection/energy_detector.py` | `rf_sentinel/detection/energy.py` | Renombrar | |
| `rf_sentinel/detection/peak_finder.py` | `rf_sentinel/detection/peak.py` | Renombrar | |
| `rf_sentinel/classification/classifier.py` | `rf_sentinel/classification/rule_based.py` | Renombrar | |
| `rf_sentinel/classification/ml_classifier.py` | `rf_sentinel/classification/ml.py` | Renombrar | Implementar |
| `rf_sentinel/classification/features.py` | `rf_sentinel/classification/features.py` | Corregir | bandwidth retorna índice, no Hz |
| `rf_sentinel/plugins/__init__.py` | `rf_sentinel/plugins/core/base.py` + `registry.py` | Dividir | Separar ABC de registry |
| `rf_sentinel/plugins/samples/energy_detection.py` | `rf_sentinel/plugins/builtin/energy_detection.py` | Mover + corregir | Eliminar duplicación con detection/ |
| `rf_sentinel/plugins/samples/template_detection.py` | `rf_sentinel/plugins/builtin/template_detection.py` | Mover | |
| `rf_sentinel/ui/main.py` | `rf_sentinel/ui/desktop/main.py` | Mover | Conectar a services |
| *(nuevo)* | `rf_sentinel/core/config.py` | Crear | Settings centralizadas |
| *(nuevo)* | `rf_sentinel/core/events.py` | Crear | Event bus |
| *(nuevo)* | `rf_sentinel/core/types.py` | Crear | Tipos compartidos |
| *(nuevo)* | `rf_sentinel/devices/registry.py` | Crear | Device discovery |
| *(nuevo)* | `rf_sentinel/devices/mock.py` | Crear | Mock para tests |
| *(nuevo)* | `rf_sentinel/database/models/__init__.py` | Crear | |
| *(nuevo)* | `rf_sentinel/database/models/capture.py` | Crear | Modelo Capture |
| *(nuevo)* | `rf_sentinel/database/models/signal.py` | Crear | Modelo Signal |
| *(nuevo)* | `rf_sentinel/database/repositories/` | Crear | Repositorios CRUD |
| *(nuevo)* | `rf_sentinel/database/session.py` | Crear | Engine + sessions |
| *(nuevo)* | `rf_sentinel/detection/base.py` | Crear | Detector ABC |
| *(nuevo)* | `rf_sentinel/classification/base.py` | Crear | Classifier ABC |
| *(nuevo)* | `rf_sentinel/services/pipeline.py` | Crear | Pipeline RF |
| *(nuevo)* | `rf_sentinel/ui/web/` | Crear | Futuro |
| *(nuevo)* | `rf_sentinel/safety/` | Crear | Límites, compliance |
| *(nuevo)* | `rf_sentinel/config/` | Crear | Settings, defaults |
| *(nuevo)* | `rf_sentinel/plugins/core/loader.py` | Crear | Auto-discovery |
| *(nuevo)* | `rf_sentinel/utils/` | Crear | Logging, validators |

---

## 3. Dependencias Entre Módulos (Dirección Permitida)

```
                    ┌─────────────┐
                    │    core/    │
                    │ config,types│
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
    │  devices/ │   │ analysis/ │   │ detection/│
    │  base ABC │   │ spectrum, │   │  base ABC │
    │ rtl,hackrf│   │ waterfall │   │threshold,  │
    └─────┬─────┘   │demodulator│   │energy,peak│
          │         └─────┬─────┘   └─────┬─────┘
          │               │                │
          │         ┌─────┴─────┐          │
          │         │classification│        │
          │         │rule_based,ml│        │
          │         │  features  │         │
          │         └─────┬─────┘          │
          │               │                │
          │         ┌─────┴─────┐          │
          │         │ services/ │          │
          │         │scan,capture│         │
          │         │export,pipe│          │
          │         └─────┬─────┘          │
          │               │                │
          │         ┌─────┴─────┐          │
          │         │ database/ │◄─────────┤
          │         │models,repo│         │
          │         └─────┬─────┘          │
          │               │                │
          │         ┌─────┴─────┐          │
          │         │   api/    │          │
          │         │ routers   │          │
          │         └─────┬─────┘          │
          │               │                │
          │         ┌─────┴─────┐          │
          │         │    ui/    │          │
          │         │desktop,web│          │
          │         └───────────┘          │
          │                               │
    ┌─────┴─────┐                   ┌─────┴─────┐
    │ plugins/  │                   │ safety/   │
    │core,bultin│                   │limits,wc  │
    └───────────┘                   └───────────┘
```

**Regla de dependencia:** Un módulo puede importar solo de módulos en niveles inferiores o iguales. Nunca hacia arriba.

---

## 4. Responsabilidades por Módulo

| Módulo | Responsabilidad | Principio |
|--------|-----------------|-----------|
| `core/` | Configuración, tipos, eventos, excepciones | Solo dependencias stdlib |
| `devices/` | Abstracción SDR, discovery, drivers | Ninguna dependencia de negocio |
| `analysis/` | FFT, waterfall, demodulación, filtros | Solo numpy/scipy |
| `detection/` | Algoritmos de detección de señales | Solo numpy + analysis |
| `classification/` | Clasificación rule-based y ML | Solo numpy/sklearn + detection |
| `database/` | Modelos ORM, sesiones, repositorios | Solo SQLAlchemy |
| `services/` | Lógica de negocio, pipelines | Depende de devices, analysis, detection, classification, database |
| `api/` | Endpoints REST, schemas Pydantic | Depende de services |
| `ui/` | Interfaces (Qt desktop + futuro web) | Depende de services o api |
| `plugins/` | Extensiones sin modificar core | Depende de interfaces ABC |
| `safety/` | Límites, compliance, emergency stop | Depende de devices |
| `config/` | Settings centralizados | Solo pydantic-settings |

---

## 5. Problemas Actuales Identificados

### 5.1 God Modules
| Módulo | Problema | Solución |
|--------|----------|----------|
| `api/main.py` | Todos los endpoints en un archivo | Separar en routers/ |
| `database/models.py` | Modelos + engine + sesiones | Separar models/ de session.py |
| `ui/main.py` | Widgets + layout + update logic | Separar widgets de lógica |

### 5.2 Código Duplicado
| Duplicación | Archivos | Solución |
|-------------|----------|----------|
| Energy detection | `detection/energy_detector.py` vs `plugins/samples/energy_detection.py` | Plugin usa `detection/energy.py` como backend |
| Peak finding | `spectrum.py:detect_peaks()` vs `detection/peak_finder.py` | `SpectrumAnalyzer` usa `PeakFinder` internamente |
| RTL-SDR / HackRF | 90% código idéntico | Extraer mixin `CommonSDRLogic` |

### 5.3 Dependencias Circulares
| Riesgo | Descripción | Solución |
|--------|-------------|----------|
| `plugins/samples/*` → `plugins/__init__` | Si plugins crecen y necesitan services | Plugins solo importan de `plugins/core/` |
| `services/` → `api/` | Si services necesitan llamar API | Nunca. API → Services, no al revés |
| `ui/` → `devices/` | Si UI necesita configurar SDR directamente | UI → Services → Devices |

### 5.4 Acoplamiento Excesivo
| Problema | Actual | Propuesto |
|----------|--------|-----------|
| API no usa services | Endpoints retornan mocks | Inyectar services en routers |
| Services no usan DB | In-memory dicts/lists | Repositories como dependencia |
| UI no usa services | Mock data en `_update_display()` | UI consume `ScanService` |
| Sin event bus | Sin comunicación entre módulos | `core/events.py` para pub/sub |

### 5.5 Módulos Gigantes / Mezcla de Responsabilidades
| Módulo | Mezcla | Separar |
|--------|--------|---------|
| `api/main.py` | Endpoints + schemas + CORS | Routers + schemas/ + dependencies |
| `database/models.py` | ORM + Engine + Session | models/ + repositories/ + session.py |
| `ui/main.py` | Widgets + Layout + Timer + Mock data | widgets/ + main_window + update_loop |

---

## 6. Extensibilidad Futura

### Nuevos SDR
- Implementar `SDRDevice` en `devices/`
- Registrar en `devices/registry.py`
- Sin cambios en analysis/detection/classification/api/ui

### Nuevas Fuentes RF
- Crear clase que implemente `SDRDevice` (file, network stream, etc.)
- Mismo contrato, mismo flujo downstream

### Nuevos Algoritmos de Detección
- Implementar `Detector` ABC en `detection/`
- Registrar como plugin en `plugins/builtin/`
- Pipeline puede usar múltiples detectores en paralelo

### Nuevas Interfaces Web
- `ui/web/app.py` consume misma API REST
- O consume `services/` directamente para web real-time
- Canvas visualizations ya modularizadas en FASE 3

### Nuevas Bases de Datos
- Implementar repositorio en `database/repositories/`
- Cambiar solo `database/session.py` y factories
- Services no cambian (usan interfaces de repositorio)

---

## 7. Riesgos de Migración

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Break de imports durante movimiento | Alta | Alto | Migración gradual con imports temporales |
| Tests rotos por reorganización | Media | Alto | Actualizar imports en tests junto con código |
| CORS mal configurado post-split | Baja | Medio | Mover CORS a `api/dependencies.py` |
| DB engine se crea en import time | Media | Medio | Mover a factory function en `session.py` |
| Plugins rotos por rename de módulos | Media | Bajo | Mantener aliases en `__init__.py` durante transición |
| UI desktop desconectada | Baja | Bajo | Conectar UI a services, no al revés |
| Incompatibilidad con GitHub Pages | Baja | Bajo | No tocar frontend en esta fase |

---

## 8. Orden de Migración Recomendado

1. **`core/`** — Sin dependencias, base de todo
2. **`devices/`** — Mover desde `sdr/`, sin dependencias internas
3. **`database/`** — Separar models de session
4. **`analysis/`** — Mover + corregir demodulator FSK
5. **`detection/`** — Renombrar + crear ABC
6. **`classification/`** — Renombrar + corregir features
7. **`services/`** — Conectar a database
8. **`plugins/core/`** — Separar ABC de registry
9. **`plugins/builtin/`** — Mover + corregir duplicación
10. **`api/routers/`** — Extraer endpoints + conectar services
11. **`ui/desktop/`** — Conectar a services
12. **`safety/`, `config/`, `utils/`** — Nuevos módulos

Cada paso es independently deployable y testeable.
