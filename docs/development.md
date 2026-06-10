# Desarrollo en RF Sentinel

## Setup Inicial

```bash
git clone https://github.com/rf-sentinel/rf-sentinel
cd rf-sentinel
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=rf_sentinel --cov-report=html

# Tests específicos
pytest tests/test_sdr.py -v
```

## Linting y Formato

```bash
# Lint
ruff check rf_sentinel tests

# Formato
ruff format rf_sentinel tests

# Chequeo de seguridad
bandit -r rf_sentinel
```

## Estructura de Tests

```
tests/
├── test_sdr.py        # Tests de dispositivos SDR
├── test_api.py        # Tests de endpoints API
├── test_analysis.py   # Tests de análisis
├── conftest.py      # Fixtures compartidas
└── __init__.py
```

## Añadir Nuevos Dispositivos SDR

1. Extiende `SDRDevice` en `rf_sentinel/sdr/base.py`
2. Implementa en `rf_sentinel/sdr/`
3. Registra en `rf_sentinel/sdr/__init__.py`
4. Añade tests

## Crear Plugins

```python
from rf_sentinel.plugins import DetectionPlugin

class MiDetector(DetectionPlugin):
    name = "mi_detector"

    async def initialize(self):
        # Setup
        pass

    def detect(self, samples):
        # Detection logic
        return []
```