# Base de datos (PostgreSQL + Alembic)

## Objetivo

Gestionar el esquema de producción con migraciones versionadas y semillas iniciales.

## Componentes

| Pieza | Ubicación |
|-------|-----------|
| Config Alembic | `backend/alembic.ini` |
| Entorno async | `backend/alembic/env.py` |
| Migración inicial | `backend/alembic/versions/001_initial_schema.py` |
| Init + migrate + seed | `backend/scripts/init_db.py` |
| Semillas | `backend/scripts/seed_db.py` |

## Tablas y relaciones

- `users` → `targets`, `scans`, `sessions`, `audit_logs`, academia
- `targets` → `scans`
- `scans` → `reports`
- `machines` → `sessions`
- Academia: `academy_courses` → `academy_lessons`
- Academia: `users` ↔ `academy_enrollments` / `academy_lesson_progress`

## Uso local

```bash
cd backend
# Con DATABASE_URL apuntando a PostgreSQL
alembic upgrade head
python scripts/seed_db.py
```

## Docker

El entrypoint del backend ejecuta automáticamente:

1. Espera a PostgreSQL
2. `alembic upgrade head` (o `stamp head` si el esquema ya existía)
3. Semillas (academia, admin, máquina de laboratorio)

```bash
docker compose up --build -d
```

## Semillas

- Cursos de la Academia RF Sentinel (5 cursos / 13 lecciones)
- Usuario admin (`SEED_ADMIN_*` en `.env`)
- Máquina de laboratorio `lab-sdr-01`
