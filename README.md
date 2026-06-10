# RF Sentinel

Plataforma Open Source para análisis de radiofrecuencia usando HackRF One y otros SDR.

[![CI](https://github.com/rf-sentinel/rf-sentinel/workflows/CI/badge.svg)](https://github.com/rf-sentinel/rf-sentinel/actions)
[![MIT License](https://img.shields.io/github/license/rf-sentinel/rf-sentinel)](LICENSE)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![CodeQL](https://github.com/rf-sentinel/rf-sentinel/workflows/CodeQL/badge.svg)](https://github.com/rf-sentinel/rf-sentinel/actions)

## Características

- **Spectrum Analyzer** en tiempo real
- **Waterfall** profesional con PyQtGraph
- Escaneo automático de frecuencias
- Detección inteligente de señales
- Clasificación automática con ML
- Dashboard moderno Qt5/Qt6
- Exportación PDF/JSON
- Historial de capturas
- Base de datos SQLite
- API REST con FastAPI
- Arquitectura modular
- Sistema de plugins extensible

## Instalación

```bash
pip install rf-sentinel
pip install rf-sentinel[hackrf]  # Con soporte HackRF
pip install rf-sentinel[rtl]    # Con soporte RTL-SDR
```

## Uso

```bash
rf-sentinel api    # Iniciar servidor API
rf-sentinel ui     # Iniciar interfaz gráfica
```

## API

```python
from rf_sentinel.api.main import app
```

Endpoints disponibles:
- `GET /health` - Estado del sistema
- `POST /scan` - Iniciar escaneo
- `GET /capture` - Listar capturas
- `POST /export/pdf` - Exportar a PDF

## Documentación

[docs.rf-sentinel.org](https://docs.rf-sentinel.org)

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md)

## Licencia

MIT License