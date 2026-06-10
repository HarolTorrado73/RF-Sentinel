(function() {
  'use strict';

  const STORAGE_KEY = 'rf-sentinel-academy-progress';

  const sections = [
    {
      id: 'sdr-fundamentals',
      title: 'SDR Fundamentals',
      icon: '📡',
      description: 'Qué es SDR, arquitectura y principios básicos del radio definido por software.',
      content: `
        <h4>¿Qué es SDR?</h4>
        <p>El <strong>Radio Definido por Software (SDR)</strong> es un sistema de comunicación donde las funciones de procesamiento de señal se implementan en software en lugar de hardware dedicado. Permite recibir, demodular y analizar señales de radio en tiempo real.</p>

        <h4>Arquitectura básica</h4>
        <p>Un sistema SDR se compone típicamente de:</p>
        <ul>
          <li><strong>Antena</strong> — capta ondas electromagnéticas del espectro RF.</li>
          <li><strong>Front-end analógico</strong> — filtros, amplificadores y mezcladores (LNA, filtros SAW, etc.).</li>
          <li><strong>Convertidor ADC</strong> — muestrea la señal analógica en digital (I/Q samples).</li>
          <li><strong>Procesamiento digital</strong> — FPGA, GPU o CPU ejecutan filtros, demoduladores y decodificadores.</li>
          <li><strong>Software</strong> — controla el hardware y aplica algoritmos DSP.</li>
        </ul>

        <h4>Principios clave</h4>
        <ul>
          <li>Muestreo por <strong>Nyquist</strong>: Fs > 2 × BW.</li>
          <li>Muestreo <strong>sub-Nyquist</strong> o <em>undersampling</em>: permite capturar bandas altas con un ADC más lento.</li>
          <li>Flujo I/Q (In-phase / Quadrature): representa la señal como números complejos.</li>
        </ul>

        <h4>Ejemplo: configuración gqrx (SDR# equivalente para Linux/macOS)</h4>
        <pre><code># Modo de recepción WFM (broadcast FM) a 100.1 MHz
# Dispositivo: HackRF One
# Ganancia LNA: 20 dB | Gain VGA: 20 dB | Gain BB: 20 dB

# Lanzar gqrx con dispositivo HackRF:
gqrx -c ~/.config/gqrx/default.conf -r hackrf

# O usando SoapySDRUtil directamente:
SoapySDRUtil --find="driver=hackrf"
SoapySDRPlay --driver=hackrf --ant=BIFAST --gain=30 --freq=100.1e6</code></pre>
      `
    },
    {
      id: 'rf-fundamentals',
      title: 'RF Fundamentals',
      icon: '📻',
      description: 'Ondas electromagnéticas, modulación, bandas de frecuencia y propagación.',
      content: `
        <h4>Ondas Electromagnéticas</h4>
        <p>Una onda de radio es un campo electromagnético oscilante que se propaga por el espacio a la velocidad de la luz (c ≈ 30 cm/ns). Sus parámetros fundamentales son:</p>
        <ul>
          <li><strong>Frecuencia (f)</strong>: ciclos por segundo (Hz). Relacionada con la longitud de onda: λ = c / f.</li>
          <li><strong>Amplitud</strong>: intensidad de la señal, se mide en dBm, dBµV o W.</li>
          <li><strong>Fase</strong>: punto en el ciclo de la señal.</li>
        </ul>

        <h4>Bandas de espectro común</h4>
        <table class="academy-table">
          <thead>
            <tr><th>Banda</th><th>Rango</th><th>Usos comunes</th></tr>
          </thead>
          <tbody>
            <tr><td>LF</td><td>30 – 300 kHz</td><td>NAVDAT, AIS</td></tr>
            <tr><td>MF</td><td>300 kHz – 3 MHz</td><td>AM broadcast, marítima</td></tr>
            <tr><td>HF</td><td>3 – 30 MHz</td><td>CB, HF Broadcasting, militares</td></tr>
            <tr><td>VHF</td><td>30 – 300 MHz</td><td>FM broadcast, ATC, VHF marine</td></tr>
            <tr><td>UHF</td><td>300 MHz – 3 GHz</td><td>GSM, LTE, Wi-Fi, GPS, TV digital</td></tr>
            <tr><td>SHF</td><td>3 – 30 GHz</td><td>Wi-Fi 5/6/7, radar, satélite</td></tr>
          </tbody>
        </table>

        <h4>Modulación</h4>
        <p>Proceso de variar un parámetro de la onda portadora para transportar información:</p>
        <ul>
          <li><strong>AM</strong> (Amplitud): variación de la amplitud. Simple, susceptible a ruido.</li>
          <li><strong>FM</strong> (Frecuencia): variación de la frecuencia. Mejor rechazo de ruido.</li>
          <li><strong>PM</strong> (Fase): variación de la fase. Usado en modos digitales.</li>
          <li><strong>ASK / FSK / PSK</strong>: versiones digitales.</li>
        </ul>

        <h4>Ejemplo: análisis con inspectrum (ANTLR)</h4>
        <pre><code># Captura en VHF y abrir en inspectrum:
$ rtl_sdr -f 145.8e6 -s 2e6 -n 2048000 sat_capture.iq
$ inspectrum sat_capture.iq
# Ajustar threshold y colormap para identificar señales. </code></pre>
      `
    },
    {
      id: 'hackrf-one',
      title: 'HackRF One',
      icon: '🔧',
      description: 'Especificaciones, uso y configuración del transceptor SDR HackRF One.',
      content: `
        <h4>Especificaciones principales</h4>
        <table class="academy-table">
          <thead>
            <tr><th>Característica</th><th>Valor</th></tr>
          </thead>
          <tbody>
            <tr><td>Rango de frecuencia</td><td>1 MHz – 6 GHz</td></tr>
            <tr><td>Ancho de banda máximo</td><td>20 MHz</td></tr>
            <tr><td>Interfaz</td><td>USB 2.0 High Speed</td></tr>
            <tr><td>Muestreo</td><td>10 MS/s (8-bit) / 20 MS/s reducido</td></tr>
            <tr><td>EIRP (TX)</td><td>Hasta +14 dBm (dependiendo de banda)</td></tr>
            <tr><td>Fabricante</td><td>Great Scott Gadgets</td></tr>
          </tbody>
        </table>

        <h4>Instalación de drivers (Windows/macOS/Linux)</h4>
        <pre><code># Instalar dependencias
$ sudo apt update && sudo apt install hackrf libhackrf-dev

# Verificar detección del hardware
$ hackrf_info

# Salida esperada:
# board_id: 2 (HackRF One) - Firmware v2018.01.1
# USB: 3.7V

# Actualizar firmware si es necesario
$ hackrf_spiflash -w hackrf_one_usb.bin

# Verificar periférico USB
$ hackrf_info
Found HackRF</code></pre>

        <h4>Configuración de ganancia</h4>
        <p>La cadena de ganancia se compone de:</p>
        <ul>
          <li><strong>LNA (Low Noise Amplifier)</strong>: 0 a 40 dB</li>
          <li><strong>VGA (Variable Gain Amplifier)</strong>: 0 a 62 dB</li>
          <li><strong>BB (Baseband)</strong>: 0 a 62 dB (solo en RX)</li>
        </ul>

        <h4>Ejemplo: usar en GNU Radio</h4>
        <pre><code># In GNU Radio Companion:
# 1. Source: OsmoSDR Source / HackRF Source
# 2. FFT sink: center freq = 433.92e6 Hz
# 3. Sample rate = 2e6
# 4. RF Gain: LNA = 30, VGA = 30, BB = 20
# 5. Bandwidth: 2 MHz</code></pre>
      `
    },
    {
      id: 'portapack-mayhem',
      title: 'PortaPack Mayhem v2.2.0',
      icon: '📲',
      description: 'Firmware, funciones avanzadas e instalación en PortaPack para HackRF One.',
      content: `
        <h4>¿Qué es PortaPack?</h4>
        <p><strong>PortaPack</strong> es un accesorio para HackRF One que acopla una pantalla táctil, controles físicos y un microcontrolador (STM32) para operación <em>standalone</em> sin necesidad de un ordenador. <strong>Mayhem</strong> es uno de los firmware personalizados más populares con más de 50 aplicaciones integradas.</p>

        <h4>Novedades v2.2.0</h4>
        <ul>
          <li>Mejora de la estabilidad en el <strong>transceptor</strong>.</li>
          <li>Filtros dinámicos en <strong>RX/TX</strong>.</li>
          <li>Soporte para <strong>grabación de I/Q directa</strong> en tarjeta microSD.</li>
          <li>Mejoras en el <strong>analizador de espectro</strong> (peak hold, waterfall).</li>
          <li>Actualización del módulo <strong>ADS-B</strong> y <strong>ACARS</strong>.</li>
        </ul>

        <h4>Instalación del firmware</h4>
        <pre><code># 1. Descargar el firmware desde GitHub:
$ git clone https://github.com/portapack-mayhem/mayhem-firmware.git
$ cd mayhem-firmware

# 2. Compilar (requiere ARM GCC toolchain)
$ make -j4

# 3. Instalar en el PortaPack (conectado por JTAG/SWD):
$ make install_portapack

# O actualizar vía Bootloader:
$ ./firmware/flash_portapack.py --port /dev/ttyACM0

# 4. Actualizar la firmware de la HackRF si es necesario:
$ hackrf_spiflash -w firmware/hackrf_usb.bin</code></pre>

        <h4>Funciones destacadas</h4>
        <ul>
          <li><strong>Spectrum Analyzer</strong>: waterfall en tiempo real, marcadores, peak hold.</li>
          <li><strong>Frequency Manager</strong>: memorias de canales, importación desde CSV.</li>
          <li><strong>Replay Attack</strong>: captura y reproducción de señales.</li>
          <li><strong>ADS-B / ACARS</strong>: seguimiento de aeronaves.</li>
          <li><strong>Tools</strong>: medidor de campo, generador de señales (TX), scrambler.</li>
        </ul>
      `
    },
    {
      id: 'signal-analysis',
      title: 'Signal Analysis',
      icon: '🔍',
      description: 'Técnicas de análisis, identificación y demodulación de señales.',
      content: `
        <h4>Técnicas de captura y análisis</h4>
        <ul>
          <li><strong>Waterfall</strong>: visualización tiempo-frecuencia ideal para detectar señales cortas o modulaciones.</li>
          <li><strong>FFT</strong>: análisis espectral en tiempo real para localizar portadoras.</li>
          <li><strong>Demodulación selectiva</strong>: hacer zoom en la banda, sintonizar y demodular.</li>
        </ul>

        <h4>Identificación automática de señales</h4>
        <p>Utiliza herramientas como <strong>inspectrum</strong>, <strong>radiosonde</strong> o <strong>Universal Radio Hacker (URH)</strong> para:</p>
        <ol>
          <li>Capturar muestras I/Q.</li>
          <li>Visualizar waterfall o constelación.</li>
          <li>Identificar parámetros: frecuencia central, ancho de banda, tasa de símbolos.</li>
          <li>Aplicar demodulación correspondiente.</li>
        </ol>

        <h4>Demodulación común</h4>
        <table class="academy-table">
          <thead>
            <tr><th>Modo</th><th>Ancho</th><th>Uso típico</th></tr>
          </thead>
          <tbody>
            <tr><td>NFM</td><td>12.5 / 25 kHz</td><td>Walkie-talkies, PMR446</td></tr>
            <tr><td>WFM</td><td>~200 kHz</td><td>FM broadcast</td></tr>
            <tr><td>AM</td><td>~10 kHz</td><td>AM broadcast, AIS</td></tr>
            <tr><td>USB/LSB</td><td>~3 kHz</td><td>HF SSB (radioafición)</td></tr>
            <tr><td>FSK</td><td>Variable</td><td>Telemetría, sensores</td></tr>
            <tr><td>LoRa / CSS</td><td>Variable</td><td>IoT, sensores de baja potencia</td></tr>
          </tbody>
        </table>

        <h4>Ejemplo: raspado de TETRA con GR-Radio</h4>
        <pre><code># GNU Radio 3.10 + gr-tetra
# PY: Ejecutar el flowgraph TETRA

const portapack_mayhem = new PortapackMayhem();
portapack_mayhem.init();

// Escanear red TETRA en banda 380-430 MHz
portapack_mayhem.analyzer.scan({
  start_mhz: 380,
  stop_mhz: 430,
  step_khz: 12.5,
  dwell_ms: 100,
  modulation: 'pi4dqpsk'
});</code></pre>
      `
    }
  ];

  function getProgress() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function saveProgress(progress) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    } catch (e) {}
  }

  function markRead(sectionId) {
    const progress = getProgress();
    if (!progress[sectionId]) {
      progress[sectionId] = true;
      saveProgress(progress);
    }
  }

  function isRead(sectionId) {
    return !!getProgress()[sectionId];
  }

  function renderAcademy(containerId) {
    const container = typeof containerId === 'string' ? document.getElementById(containerId) : containerId;
    if (!container) return;
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'academy-wrapper';

    const header = document.createElement('div');
    header.className = 'academy-header';
    header.innerHTML = `
      <h2 class="academy-title">Academy</h2>
      <p class="academy-subtitle">Aprendizaje estructurado sobre SDR y RF.</p>
      <div class="academy-progress-bar">
        <div class="academy-progress-fill" id="academyProgressFill"></div>
      </div>
      <p class="academy-progress-text" id="academyProgressText">0 / ${sections.length} secciones leídas</p>
    `;

    const grid = document.createElement('div');
    grid.className = 'academy-grid';

    sections.forEach((section) => {
      const card = document.createElement('article');
      card.className = 'academy-card';
      card.dataset.sectionId = section.id;

      const statusClass = isRead(section.id) ? 'is-read' : 'is-unread';
      const statusLabel = isRead(section.id) ? 'Leída' : 'No leída';

      card.innerHTML = `
        <div class="academy-card-header">
          <div class="academy-card-icon">${section.icon}</div>
          <div class="academy-card-meta">
            <h3 class="academy-card-title">${section.title}</h3>
            <p class="academy-card-description">${section.description}</p>
          </div>
          <button type="button" class="academy-toggle-button" data-section="${section.id}" aria-expanded="false">
            <span class="academy-toggle-label">Leer más</span>
            <span class="academy-toggle-icon" aria-hidden="true"></span>
          </button>
        </div>
        <div class="academy-progress-indicator ${statusClass}" data-progress-section="${section.id}">
          <span class="academy-progress-dot"></span>
          <span class="academy-progress-label">${statusLabel}</span>
        </div>
        <div class="academy-card-body" data-body-section="${section.id}" hidden>
          <div class="academy-card-content">
            ${section.content}
            <div class="academy-card-footer">
              <button type="button" class="academy-mark-read-button" data-section="${section.id}">
                Marcar como leído
              </button>
            </div>
          </div>
        </div>
      `;

      grid.appendChild(card);
    });

    wrapper.appendChild(header);
    wrapper.appendChild(grid);
    container.appendChild(wrapper);
    updateProgressBar();

    wrapper.addEventListener('click', handleAcademyClick);
  }

  function updateProgressBar() {
    const fill = document.getElementById('academyProgressFill');
    const text = document.getElementById('academyProgressText');
    if (!fill || !text) return;

    const readCount = sections.filter((s) => isRead(s.id)).length;
    const pct = sections.length ? (readCount / sections.length) * 100 : 0;
    fill.style.width = pct.toFixed(2) + '%';
    text.textContent = readCount + ' / ' + sections.length + ' secciones leídas';
  }

  function handleAcademyClick(event) {
    const target = event.target;

    const toggleButton = target.closest('.academy-toggle-button');
    if (toggleButton) {
      const sectionId = toggleButton.dataset.section;
      if (sectionId) {
        toggleSection(sectionId);
      }
      return;
    }

    const markButton = target.closest('.academy-mark-read-button');
    if (markButton) {
      const sectionId = markButton.dataset.section;
      if (sectionId) {
        markRead(sectionId);
        refreshCard(sectionId);
        updateProgressBar();
      }
      return;
    }
  }

  function toggleSection(sectionId) {
    const card = document.querySelector('.academy-card[data-section-id="' + sectionId + '"]');
    if (!card) return;

    const body = card.querySelector('.academy-card-body[data-body-section="' + sectionId + '"]');
    const button = card.querySelector('.academy-toggle-button[data-section="' + sectionId + '"]');
    if (!body || !button) return;

    const isExpanded = !body.hidden;
    body.hidden = isExpanded;
    button.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');

    const label = button.querySelector('.academy-toggle-label');
    if (label) {
      label.textContent = isExpanded ? 'Leer más' : 'Leer menos';
    }

    if (!isExpanded) {
      markRead(sectionId);
      refreshCard(sectionId);
      updateProgressBar();
    }
  }

  function refreshCard(sectionId) {
    const indicator = document.querySelector('.academy-progress-indicator[data-progress-section="' + sectionId + '"]');
    if (!indicator) return;

    const read = isRead(sectionId);
    indicator.classList.toggle('is-read', read);
    indicator.classList.toggle('is-unread', !read);

    const label = indicator.querySelector('.academy-progress-label');
    if (label) {
      label.textContent = read ? 'Leída' : 'No leída';
    }
  }

  function initAcademy(containerId) {
    if (typeof containerId === 'string') {
      const container = document.getElementById(containerId);
      if (container) {
        renderAcademy(container);
        return;
      }
    }

    renderAcademy(containerId);
  }

  const academy = {
    initAcademy: initAcademy,
    toggleSection: toggleSection,
    sections: sections,
    markRead: markRead
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = academy;
  } else if (typeof window !== 'undefined') {
    window.Academy = academy;
  }
})();
