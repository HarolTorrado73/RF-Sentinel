# Academia RF Sentinel (FASE 4)

## Objetivo

Convertir RF Sentinel en una plataforma educativa sobre SDR y radiofrecuencia orientada a:

- Educacion
- Investigacion
- Aprendizaje responsable

## Contenido implementado

La Academia integrada en la web incluye 5 cursos interactivos:

1. Fundamentos de RF
2. Conceptos SDR
3. HackRF y uso responsable
4. Analisis de senales
5. Integracion de hardware

Cada curso contiene:

- Material educativo estructurado
- Ejemplo visual/tecnico
- Micro-quiz de evaluacion

## Funcionalidades

- Progreso del usuario persistente en localStorage
- Barra de avance global por cursos completados
- Estado por curso: lectura, quiz y completado
- Exportacion de progreso a JSON

## Principios de seguridad y legalidad

RF Sentinel Academy excluye explicitamente:

- Interferencia intencional
- Actividades ilegales

El enfoque es academico, de laboratorio y analisis responsable de senales.

## Integracion tecnica

- Contenido y logica: `assets/js/academy.js`
- Estilos de la academia: `assets/css/main.css`
- Seccion integrada en landing web: `index.html`
- Inicializacion en runtime: `assets/js/main.js`
