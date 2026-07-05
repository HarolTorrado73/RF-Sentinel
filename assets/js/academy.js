(function () {
  'use strict';

  const STORAGE_KEY = 'rf-sentinel-academy-progress-v2';

  const sections = [
    {
      id: 'rf-fundamentos',
      title: 'Fundamentos de RF',
      icon: 'RF',
      description: 'Frecuencia, longitud de onda, potencia y propagacion en sistemas reales.',
      content:
        '<h4>Conceptos clave</h4>' +
        '<p>La radiofrecuencia describe ondas electromagneticas usadas para comunicacion y medicion. Una idea central es la relacion entre frecuencia y longitud de onda.</p>' +
        '<ul><li>Frecuencia (Hz): numero de ciclos por segundo.</li><li>Longitud de onda (m): distancia de un ciclo completo.</li><li>Potencia (dBm): nivel relativo de energia de la senal.</li></ul>' +
        '<pre><code>Relacion fundamental\nlambda = c / f\n\nEjemplo:\nsi f = 100 MHz, lambda ~ 3 m</code></pre>' +
        '<p class="academy-note">Aprendizaje responsable: observar y analizar no implica transmitir ni interferir.</p>',
      quiz: {
        question: 'Si la frecuencia aumenta, que ocurre normalmente con la longitud de onda?',
        options: [
          'Tambien aumenta',
          'Permanece igual',
          'Disminuye',
          'Depende solo de la potencia'
        ],
        correctIndex: 2,
        explanation: 'Con c constante, al subir f, lambda = c/f disminuye.'
      }
    },
    {
      id: 'sdr-conceptos',
      title: 'Conceptos SDR',
      icon: 'SDR',
      description: 'Arquitectura I/Q, ADC, tasa de muestreo y flujo de procesamiento digital.',
      content:
        '<h4>De hardware fijo a software flexible</h4>' +
        '<p>En SDR, funciones antes implementadas en hardware dedicado se mueven a software: filtros, deteccion, demodulacion y visualizacion.</p>' +
        '<ol><li>Antena y front-end analogico.</li><li>Conversion ADC.</li><li>Muestras I/Q complejas.</li><li>DSP en software.</li></ol>' +
        '<pre><code>Cadena minima\nAntena -> LNA/Filtro -> ADC -> I/Q -> FFT -> Detector</code></pre>' +
        '<p class="academy-note">Objetivo educativo: entender procesamiento de senales para investigacion y aprendizaje.</p>',
      quiz: {
        question: 'Que representan las muestras I/Q?',
        options: [
          'Solo amplitud',
          'Componente en fase y en cuadratura',
          'Solo ruido termico',
          'Frecuencia en formato de texto'
        ],
        correctIndex: 1,
        explanation: 'I/Q modela la senal compleja con dos componentes ortogonales.'
      }
    },
    {
      id: 'hackrf-responsable',
      title: 'HackRF y uso responsable',
      icon: 'HW',
      description: 'Buenas practicas de recepcion, calibracion y cumplimiento normativo.',
      content:
        '<h4>Uso seguro y legal</h4>' +
        '<p>RF Sentinel prioriza recepcion, analisis y educacion. Antes de operar hardware, verifica las reglas locales y las bandas permitidas.</p>' +
        '<ul><li>Trabaja primero en modo RX (recepcion).</li><li>Documenta frecuencias de laboratorio y objetivos de prueba.</li><li>Evita cualquier accion que degrade servicios de terceros.</li></ul>' +
        '<pre><code>Checklist de laboratorio\n[ ] Objetivo de prueba definido\n[ ] Entorno controlado\n[ ] Registro de parametros\n[ ] Cumplimiento regulatorio confirmado</code></pre>' +
        '<p class="academy-warning">No incluir: interferencia, bloqueo de senales o actividades ilegales.</p>',
      quiz: {
        question: 'Cual es la primera recomendacion para aprendizaje seguro con SDR?',
        options: [
          'Transmitir de inmediato para medir alcance',
          'Operar en recepcion y validar normativa',
          'Subir ganancia al maximo siempre',
          'Deshabilitar filtros para captar todo'
        ],
        correctIndex: 1,
        explanation: 'El aprendizaje responsable inicia con recepcion y marco legal claro.'
      }
    },
    {
      id: 'analisis-senales',
      title: 'Analisis de senales',
      icon: 'DSP',
      description: 'FFT, waterfall, umbrales y lectura de patrones de espectro.',
      content:
        '<h4>Lectura visual y metrica</h4>' +
        '<p>El analisis combina vistas en frecuencia y tiempo-frecuencia para detectar eventos de interes.</p>' +
        '<table class="academy-table"><thead><tr><th>Herramienta</th><th>Que aporta</th></tr></thead><tbody><tr><td>FFT</td><td>Distribucion de energia por frecuencia</td></tr><tr><td>Waterfall</td><td>Evolucion temporal de la actividad espectral</td></tr><tr><td>Detector</td><td>Eventos por umbral o energia</td></tr></tbody></table>' +
        '<pre><code>Interpretacion basica\nPico estable + ancho estrecho -> posible portadora\nEvento corto y ancho -> posible rafaga/transitorio</code></pre>',
      quiz: {
        question: 'Que visualizacion muestra mejor cambios de senal a lo largo del tiempo?',
        options: ['Solo lista de valores', 'Waterfall', 'Tabla de rutas', 'Historial de commits'],
        correctIndex: 1,
        explanation: 'Waterfall combina tiempo y frecuencia para ver dinamica espectral.'
      }
    },
    {
      id: 'integracion-hardware',
      title: 'Integracion de hardware',
      icon: 'SYS',
      description: 'Dispositivos, drivers, capas de servicios y validacion de pipeline.',
      content:
        '<h4>Arquitectura modular aplicada</h4>' +
        '<p>La integracion en RF Sentinel separa dispositivos, analisis, deteccion, clasificacion y servicios para escalar sin acoplamientos fuertes.</p>' +
        '<ul><li>devices/: control de SDR y registro.</li><li>services/: pipeline de negocio.</li><li>api/: exposicion REST para dashboard y automatizacion.</li></ul>' +
        '<pre><code>Flujo recomendado\nDeviceRegistry -> ScanService -> DetectionPipeline -> API/UI</code></pre>' +
        '<p class="academy-note">La modularidad acelera investigacion reproducible y colaborativa.</p>',
      quiz: {
        question: 'Que beneficio principal aporta separar devices, services y api?',
        options: [
          'Mas lineas de codigo sin ventaja',
          'Escalabilidad y mantenibilidad',
          'Eliminar necesidad de pruebas',
          'Ocultar errores de integracion'
        ],
        correctIndex: 1,
        explanation: 'La separacion de responsabilidades reduce acoplamiento y facilita evolucion.'
      }
    }
  ];

  function defaultState() {
    return { read: {}, quiz: {} };
  }

  function getState() {
    try {
      const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      return {
        read: parsed.read || {},
        quiz: parsed.quiz || {}
      };
    } catch (_error) {
      return defaultState();
    }
  }

  function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function markRead(sectionId) {
    const state = getState();
    state.read[sectionId] = true;
    saveState(state);
  }

  function saveQuiz(sectionId, isCorrect) {
    const state = getState();
    state.quiz[sectionId] = !!isCorrect;
    saveState(state);
  }

  function isRead(sectionId) {
    return !!getState().read[sectionId];
  }

  function isQuizPassed(sectionId) {
    return !!getState().quiz[sectionId];
  }

  function sectionCompletion(sectionId) {
    return isRead(sectionId) && isQuizPassed(sectionId);
  }

  function completionStats() {
    const completed = sections.filter((s) => sectionCompletion(s.id)).length;
    return {
      completed,
      total: sections.length,
      percent: sections.length ? (completed / sections.length) * 100 : 0
    };
  }

  function renderSectionCard(section) {
    const readLabel = isRead(section.id) ? 'Leida' : 'No leida';
    const quizLabel = isQuizPassed(section.id) ? 'Quiz aprobado' : 'Quiz pendiente';
    const doneLabel = sectionCompletion(section.id) ? 'Completado' : 'En progreso';

    return (
      '<article class="academy-card" data-section-id="' + section.id + '">' +
      '<div class="academy-card-header">' +
      '<div class="academy-card-icon">' + section.icon + '</div>' +
      '<div class="academy-card-meta">' +
      '<h3 class="academy-card-title">' + section.title + '</h3>' +
      '<p class="academy-card-description">' + section.description + '</p>' +
      '</div>' +
      '<button type="button" class="academy-toggle-button" data-section="' + section.id + '" aria-expanded="false">Abrir curso</button>' +
      '</div>' +
      '<div class="academy-status-row">' +
      '<span class="academy-chip">Lectura: ' + readLabel + '</span>' +
      '<span class="academy-chip">Quiz: ' + quizLabel + '</span>' +
      '<span class="academy-chip academy-chip--strong">Estado: ' + doneLabel + '</span>' +
      '</div>' +
      '<div class="academy-card-body" data-body-section="' + section.id + '" hidden>' +
      '<div class="academy-card-content">' + section.content + '</div>' +
      '<div class="academy-quiz" data-quiz-section="' + section.id + '">' +
      '<h4>Micro-quiz</h4>' +
      '<p class="academy-quiz-question">' + section.quiz.question + '</p>' +
      '<div class="academy-quiz-options">' +
      section.quiz.options.map(function (option, index) {
        return '<label><input type="radio" name="quiz-' + section.id + '" value="' + index + '"> ' + option + '</label>';
      }).join('') +
      '</div>' +
      '<div class="academy-quiz-actions">' +
      '<button type="button" class="academy-check-quiz" data-section="' + section.id + '">Evaluar</button>' +
      '<button type="button" class="academy-mark-read-button" data-section="' + section.id + '">Marcar lectura</button>' +
      '</div>' +
      '<p class="academy-quiz-feedback" data-feedback-section="' + section.id + '"></p>' +
      '</div>' +
      '</div>' +
      '</article>'
    );
  }

  function renderAcademy(containerId) {
    const container = typeof containerId === 'string' ? document.getElementById(containerId) : containerId;
    if (!container) {
      return;
    }

    const stats = completionStats();

    container.innerHTML =
      '<div class="academy-wrapper">' +
      '<div class="academy-header">' +
      '<h2 class="academy-title">Academia RF Sentinel</h2>' +
      '<p class="academy-subtitle">Cursos interactivos para educacion, investigacion y aprendizaje responsable en SDR/RF.</p>' +
      '<div class="academy-safety-banner">Uso responsable: no interferencia, no actividades ilegales, enfoque academico y de laboratorio.</div>' +
      '<div class="academy-progress-bar"><div class="academy-progress-fill" id="academyProgressFill" style="width: ' + stats.percent.toFixed(2) + '%;"></div></div>' +
      '<p class="academy-progress-text" id="academyProgressText">' + stats.completed + ' / ' + stats.total + ' cursos completados</p>' +
      '<button type="button" id="academy-export-progress" class="academy-export-button">Exportar progreso (JSON)</button>' +
      '</div>' +
      '<div class="academy-grid">' + sections.map(renderSectionCard).join('') + '</div>' +
      '</div>';

    container.addEventListener('click', handleAcademyClick);
  }

  function refreshProgressUI() {
    const stats = completionStats();
    const fill = document.getElementById('academyProgressFill');
    const text = document.getElementById('academyProgressText');

    if (fill) {
      fill.style.width = stats.percent.toFixed(2) + '%';
    }
    if (text) {
      text.textContent = stats.completed + ' / ' + stats.total + ' cursos completados';
    }

    sections.forEach(function (section) {
      const card = document.querySelector('.academy-card[data-section-id="' + section.id + '"]');
      if (!card) {
        return;
      }

      const chips = card.querySelectorAll('.academy-chip');
      if (chips.length >= 3) {
        chips[0].textContent = 'Lectura: ' + (isRead(section.id) ? 'Leida' : 'No leida');
        chips[1].textContent = 'Quiz: ' + (isQuizPassed(section.id) ? 'Quiz aprobado' : 'Quiz pendiente');
        chips[2].textContent = 'Estado: ' + (sectionCompletion(section.id) ? 'Completado' : 'En progreso');
      }
    });
  }

  function toggleSection(sectionId) {
    const card = document.querySelector('.academy-card[data-section-id="' + sectionId + '"]');
    if (!card) {
      return;
    }

    const body = card.querySelector('.academy-card-body[data-body-section="' + sectionId + '"]');
    const button = card.querySelector('.academy-toggle-button[data-section="' + sectionId + '"]');
    if (!body || !button) {
      return;
    }

    const expanded = !body.hidden;
    body.hidden = expanded;
    button.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    button.textContent = expanded ? 'Abrir curso' : 'Cerrar curso';

    if (!expanded) {
      markRead(sectionId);
      refreshProgressUI();
    }
  }

  function evaluateQuiz(sectionId) {
    const section = sections.find(function (s) {
      return s.id === sectionId;
    });
    if (!section) {
      return;
    }

    const selected = document.querySelector('input[name="quiz-' + sectionId + '"]:checked');
    const feedback = document.querySelector('[data-feedback-section="' + sectionId + '"]');
    if (!selected || !feedback) {
      if (feedback) {
        feedback.textContent = 'Selecciona una opcion antes de evaluar.';
      }
      return;
    }

    const answer = Number(selected.value);
    const correct = answer === section.quiz.correctIndex;
    saveQuiz(sectionId, correct);

    feedback.textContent = correct
      ? 'Correcto. ' + section.quiz.explanation
      : 'Respuesta incorrecta. ' + section.quiz.explanation;
    feedback.classList.toggle('is-success', correct);
    feedback.classList.toggle('is-error', !correct);

    refreshProgressUI();
  }

  function exportProgress() {
    const payload = {
      generated_at: new Date().toISOString(),
      academy: 'RF Sentinel',
      progress: getState(),
      stats: completionStats()
    };

    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'rf-sentinel-academy-progress.json';
    link.click();
    URL.revokeObjectURL(url);
  }

  function handleAcademyClick(event) {
    const target = event.target;

    if (target.id === 'academy-export-progress') {
      exportProgress();
      return;
    }

    const toggleButton = target.closest('.academy-toggle-button');
    if (toggleButton && toggleButton.dataset.section) {
      toggleSection(toggleButton.dataset.section);
      return;
    }

    const markButton = target.closest('.academy-mark-read-button');
    if (markButton && markButton.dataset.section) {
      markRead(markButton.dataset.section);
      refreshProgressUI();
      return;
    }

    const quizButton = target.closest('.academy-check-quiz');
    if (quizButton && quizButton.dataset.section) {
      evaluateQuiz(quizButton.dataset.section);
    }
  }

  function initAcademy(containerId) {
    renderAcademy(containerId);
  }

  const academy = {
    initAcademy,
    toggleSection,
    markRead,
    sections
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = academy;
  } else if (typeof window !== 'undefined') {
    window.Academy = academy;
  }
})();
