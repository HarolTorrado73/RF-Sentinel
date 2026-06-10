# RF Sentinel

<p align="center">
  <img src="assets/banner/rf-sentinel-hero-banner.webp" alt="RF Sentinel Hero Banner" width="100%">
</p>

<p align="center">
  <img src="assets/branding/rf-sentinel-logo.webp" alt="RF Sentinel Logo" width="200">
</p>

[![CI](https://github.com/rf-sentinel/rf-sentinel/workflows/CI/badge.svg)](https://github.com/rf-sentinel/rf-sentinel/actions)
[![MIT License](https://img.shields.io/github/license/rf-sentinel/rf-sentinel)](LICENSE)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![CodeQL](https://github.com/rf-sentinel/rf-sentinel/workflows/CodeQL/badge.svg)](https://github.com/rf-sentinel/rf-sentinel/actions)
[![Coverage](https://img.shields.io/badge/coverage-80%25%2B-brightgreen.svg)]()
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9C%93-success.svg)]()

Plataforma Open Source para análisis de radiofrecuencia usando HackRF One y otros SDR.

## Features

| <img src="assets/dashboard/spectrum-analyzer.webp" width="200"> | <img src="assets/dashboard/waterfall-monitor.webp" width="200"> | <img src="assets/dashboard/signal-detection.webp" width="200"> |
|:---:|:---:|:---:|
| **Spectrum Analyzer** en tiempo real | **Waterfall** profesional con PyQtGraph | **Detección** inteligente de señales |

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

## Visual Tour

### Spectrum Analyzer
<p>
<img src="assets/dashboard/spectrum-analyzer.webp" alt="Spectrum Analyzer" loading="lazy" width="100%">
</p>

### Waterfall Monitor
<p>
<img src="assets/dashboard/waterfall-monitor.webp" alt="Waterfall Monitor" loading="lazy" width="100%">
</p>

### Signal Detection
<p>
<img src="assets/dashboard/signal-detection.webp" alt="Signal Detection" loading="lazy" width="100%">
</p>

## Dashboard Showcase

<p align="center">
  <img src="assets/dashboard/dashboard-overview.webp" alt="Dashboard Overview" loading="lazy" width="100%">
</p>

## Architecture

<p align="center">
  <img src="assets/architecture/rf-sentinel-architecture.webp" alt="RF Sentinel Architecture" loading="lazy" width="100%">
</p>

## Screenshots Gallery

| Dashboard | Waterfall | Detection |
|:---:|:---:|:---:|
| <img src="assets/dashboard/dashboard-overview.webp" loading="lazy"> | <img src="assets/dashboard/waterfall-monitor.webp" loading="lazy"> | <img src="assets/dashboard/signal-detection.webp" loading="lazy"> |

## Roadmap

Ver [ROADMAP.md](ROADMAP.md) para planificación de 12 meses.

[![Roadmap Status](https://img.shields.io/badge/Roadmap-Q1%202025%20%7C%20Q2%202025%20%7C%20Q3%202025%20%7C%20Q4%202025-blue)]()

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

## Social

<p>
<a href="https://github.com/rf-sentinel/rf-sentinel">
  <img src="assets/social/social-preview.webp" alt="Social Preview" loading="lazy" width="300">
</a>
<a href="https://linkedin.com/company/rf-sentinel">
  <img src="assets/social/linkedin-showcase.webp" alt="LinkedIn Showcase" loading="lazy" width="300">
</a>
</p>