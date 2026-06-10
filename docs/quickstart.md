# RF Sentinel Documentation

## Instalación

### Requisitos
- Python 3.13+
- HackRF One + drivers (opcional)
- RTL-SDR + drivers (opcional)

### Instalación
```bash
pip install -e ".[dev,hackrf,rtl]"
```

## Arquitectura

El sistema está compuesto por:

- **rf_sentinel.api**: API REST con FastAPI
- **rf_sentinel.sdr**: Abstracción de dispositivos SDR
- **rf_sentinel.analysis**: Análisis de espectro y waterfall
- **rf_sentinel.detection**: Detección de señales
- **rf_sentinel.classification**: Clasificación de modulaciones
- **rf_sentinel.database**: Modelos SQLite
- **rf_sentinel.services**: Lógica de negocio
- **rf_sentinel.plugins**: Sistema extensible

## API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| /health | GET | Estado del sistema |
| /scan | POST | Iniciar escaneo |
| /detect | POST | Detectar señales |
| /classify | POST | Clasificar señal |
| /capture | POST/GET | Gestión de capturas |
| /export/pdf | POST | Exportar a PDF |
| /export/json | POST | Exportar a JSON |

## Desarrollo

```bash
# Tests
pytest --cov=rf_sentinel

# Lint
ruff check .
ruff format .

# Security
bandit -r rf_sentinel
```