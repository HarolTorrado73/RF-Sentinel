# Changelog

All notable changes to RF Sentinel will be documented in this file.

## [Unreleased]

### Added
- Fase 3 de arquitectura modular completada con `DetectionPipeline` en `rf_sentinel/services/pipeline.py`.
- Alias de configuracion modular en `rf_sentinel/config/settings.py`.
- Placeholder de interfaz web en `rf_sentinel/ui/web/__init__.py`.
- Pruebas de arquitectura modular y plugins en `tests/test_phase3_architecture.py`.

### Changed
- Inyeccion de dependencias API con instancias compartidas para services, pipeline y registry en `rf_sentinel/api/dependencies.py`.
- Endpoints de captura, deteccion, clasificacion y exportacion alineados a contratos de request en `rf_sentinel/api/routers/*`.
- Correccion de timestamp UTC en `rf_sentinel/services/capture_service.py`.
- Esquemas API mejorados con request models y defaults seguros en `rf_sentinel/api/schemas/__init__.py`.

## [0.1.0] - 2025-01-15

### Added
- Initial release
- Spectrum Analyzer con PyQtGraph
- Waterfall display
- API REST con FastAPI
- Soporte HackRF One
- Soporte RTL-SDR
- SQLite database
- Sistema de plugins
- GitHub Actions CI
- CodeQL security analysis