# Academia RF Sentinel (FASE 4)

## Objetivo

Convertir RF Sentinel en una plataforma educativa sobre SDR y radiofrecuencia orientada a:

- Educación
- Investigación
- Aprendizaje responsable

## Contenido implementado

La Academia incluye **5 cursos** y **13 lecciones** interactivas:

| Tema | Curso | Lecciones |
|------|-------|-----------|
| RF | Fundamentos de Radiofrecuencia | 3 |
| SDR | Conceptos de SDR | 2 |
| HackRF | Uso responsable | 3 |
| Señales | Análisis de señales | 3 |
| Hardware | Integración de hardware | 2 |

Cada lección contiene:

- Material educativo en markdown
- Ejemplo visual (espectro, forma de onda o diagrama)
- Micro-quiz de evaluación (3 preguntas, mínimo 70% para aprobar)

## Funcionalidades

- Catálogo de cursos y detalle de lecciones
- Matrícula y progreso de usuario persistente en servidor (PostgreSQL / SQLite)
- Barras de avance por curso y resumen en **Mi aprendizaje**
- Reintento de quiz tras reprobar
- Exportación del progreso a JSON
- Banner y disclaimers de uso responsable

## Principios de seguridad y legalidad

RF Sentinel Academy excluye explícitamente:

- Interferencia intencional
- Jamming
- Actividades ilegales

El enfoque es académico, de laboratorio y análisis responsable de señales (prioridad: recepción pasiva).

## Integración técnica

### Frontend React (`frontend/`)

- Rutas: `/academy`, `/academy/courses/:slug`, `/academy/courses/:slug/lessons/:lessonSlug`, `/academy/my-learning`
- Componentes: `QuizWidget`, visualizadores, `ProgressBar`, `ResponsibleUseBanner`
- Store: `frontend/src/stores/academyStore.ts`

### Backend FastAPI (`backend/`)

- API: `/api/v1/academy/*`
- Seed de contenido: `backend/app/data/academy_content.py`
- Servicio: `backend/app/services/academy.py` (seed + sync de material educativo)

### Landing estática (promocional)

La landing (`index.html` + `assets/js/academy.js`) mantiene una demo educativa local.
La experiencia completa con progreso en servidor vive en el frontend React.
