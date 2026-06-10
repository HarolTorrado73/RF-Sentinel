# Arquitectura de RF Sentinel

## Visión General

RF Sentinel es una plataforma modular para análisis de radiofrecuencia con arquitectura basada en plugins.

## Módulos

```
rf_sentinel/
├── api/           # FastAPI REST endpoints
├── sdr/           # Device drivers (HackRF, RTL-SDR)
├── analysis/      # Spectrum/Waterfall processing
├── detection/     # Signal detection algorithms
├── classification/ # Modulation classification
├── database/      # SQLite models with SQLAlchemy
├── services/      # Business logic layer
├── plugins/       # Extensible plugin system
└── ui/            # Qt/PyQtGraph dashboard
```

## Diagrama de Flujo

```
+-----------------+     +-------------+     +-------------+
|    HackRF/RTL   |---->|   Capture   |---->|  Analysis   |
+-----------------+     +-------------+     +-------------+
                                |                  |
                                v                  v
                        +---------+---------+  +-----+------+
                        |  Detection      |  | Waterfall  |
                        +---------+---------+  +-----------+
                                |
                                v
                        +---------+---------+
                        | Classification    |
                        +-------------------+
                                |
                                v
                        +---------+---------+
                        |  Database         |
                        +-------------------+
```

## Plugin System

Los plugins extienden la funcionalidad:

```python
# Estructura de un plugin
class MyPlugin(DetectionPlugin):
    async def initialize(self): ...
    async def cleanup(self): ...
    def process(self, data): ...
    def detect(self, samples): ...
```

Tipos de plugins:
- **DetectionPlugin**: Detecta señales
- **ClassificationPlugin**: Clasifica modulaciones
- **ExportPlugin**: Exporta formatos