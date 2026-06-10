# Contributing to RF Sentinel

Gracias por contribuir a RF Sentinel.

## Development Setup

```bash
pip install -e ".[dev]"
pre-commit install
```

## Testing

```bash
pytest
pytest --cov=rf_sentinel
```

## Linting

```bash
ruff check .
ruff format .
bandit -r rf_sentinel
```

## Pull Request Process

1. Fork el repositorio
2. Crea feature branch
3. Ejecuta tests y linting
4. Envía PR con descripción clara

## Code Style

- Python 3.13+
- Type hints obligatorias
- Docstrings en español/inglés
- Tests con coverage > 80%

## Report Issues

Usa GitHub Issues para bugs y feature requests.