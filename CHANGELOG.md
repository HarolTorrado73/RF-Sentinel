# Changelog

All notable changes to RF Sentinel will be documented in this file.

## [Unreleased]

### Added
- Fase 3 de arquitectura modular completada con `DetectionPipeline` en `rf_sentinel/services/pipeline.py`.
- Alias de configuracion modular en `rf_sentinel/config/settings.py`.
- Placeholder de interfaz web en `rf_sentinel/ui/web/__init__.py`.
- Pruebas de arquitectura modular y plugins en `tests/test_phase3_architecture.py`.
- Fase 4 Academia RF Sentinel en frontend React + API `/api/v1/academy` (5 cursos, 13 lecciones, quizzes, visualizadores y progreso servidor).
- Exportacion de progreso de academia a JSON desde **Mi aprendizaje**.
- Reintento de quiz tras reprobar y quizzes ampliados (3 preguntas por leccion).
- Material educativo documentado en `docs/academy.md`.
- Infraestructura Docker Compose (backend, frontend, PostgreSQL, Redis).
- Migraciones Alembic + semillas iniciales para PostgreSQL (`docs/database.md`).

### Changed
- Inyeccion de dependencias API con instancias compartidas para services, pipeline y registry en `rf_sentinel/api/dependencies.py`.
- Endpoints de captura, deteccion, clasificacion y exportacion alineados a contratos de request en `rf_sentinel/api/routers/*`.
- Correccion de timestamp UTC en `rf_sentinel/services/capture_service.py`.
- Esquemas API mejorados con request models y defaults seguros en `rf_sentinel/api/schemas/__init__.py`.
- Documentacion de academia actualizada al stack React/API (la landing estatica queda como demo promocional).
- Sync de material educativo de academia sin perder progreso de usuario.
- Esquema de base de datos gestionado por Alembic en lugar de `create_all` en el arranque de la API.
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