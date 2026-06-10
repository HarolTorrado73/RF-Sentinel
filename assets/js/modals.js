const modulesData = {
  api: {
    title: "API Layer",
    description: "Capa REST y WebSocket con FastAPI. Autenticación JWT, rate limiting, OpenAPI automática.",
    tech: ["FastAPI", "Pydantic", "WebSockets", "JWT", "Uvicorn"],
    links: [{ label: "Database", target: "database" }, { label: "Services", target: "services" }]
  },
  sdr: {
    title: "SDR Drivers",
    description: "HackRF One & RTL-SDR support. Control de sintonización, ganancia, streaming I/Q continuo.",
    tech: ["Python 3.13", "HackRF / RTL-SDR", "SoapySDR", "NumPy", "SciPy"],
    links: [{ label: "Analysis", target: "analysis" }, { label: "Plugins", target: "plugins" }]
  },
  analysis: {
    title: "Analysis Engine",
    description: "DSP en tiempo real. FFT, filtros FIR/IIR, detección de energía, estimación de frecuencia.",
    tech: ["NumPy", "SciPy", "scikit-learn", "Numba"],
    links: [{ label: "Detection", target: "detection" }, { label: "SDR", target: "sdr" }]
  },
  detection: {
    title: "Detection Module",
    description: "Detección de eventos RF usando modelos ML y reglas configurables. Nuevas señales, cambios espectrales.",
    tech: ["scikit-learn", "XGBoost", "HDBSCAN", "PyOD"],
    links: [{ label: "Classification", target: "classification" }, { label: "Services", target: "services" }]
  },
  classification: {
    title: "Classifier",
    description: "Clasificador multi-etiqueta para identificar protocolos RF: WiFi, Bluetooth, Zigbee, LoRa, GSM.",
    tech: ["Random Forest", "SVM", "PyTorch", "MLflow"],
    links: [{ label: "Detection", target: "detection" }, { label: "Plugins", target: "plugins" }]
  },
  database: {
    title: "Database Layer",
    description: "Persistencia multi-backend con SQLite offline y PostgreSQL para producción. Migraciones automáticas.",
    tech: ["SQLite", "PostgreSQL", "SQLAlchemy 2.0", "Redis"],
    links: [{ label: "API", target: "api" }, { label: "Services", target: "services" }]
  }
};

const Modals = (() => {
  function open(moduleName) {
    const data = modulesData[moduleName];
    if (!data) return;

    const overlay = document.getElementById('modal-overlay');
    const titleEl = document.getElementById('modal-title');
    const descEl = document.getElementById('modal-description');
    const techList = document.getElementById('modal-tech-list');
    const linksList = document.getElementById('modal-links-list');

    if (!overlay || !titleEl) return;

    titleEl.textContent = data.title;
    descEl.textContent = data.description;

    techList.innerHTML = '';
    data.tech.forEach(t => {
      const li = document.createElement('li');
      li.className = 'tech-tag';
      li.textContent = t;
      techList.appendChild(li);
    });

    linksList.innerHTML = '';
    data.links.forEach(link => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#';
      a.textContent = link.label;
      a.onclick = (e) => {
        e.preventDefault();
        close();
        setTimeout(() => {
          const target = document.getElementById(link.target + '-card');
          if (target) target.scrollIntoView({ behavior: 'smooth' });
        }, 300);
      };
      li.appendChild(a);
      linksList.appendChild(li);
    });

    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    const overlay = document.getElementById('modal-overlay');
    if (overlay) {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }
  }

  function init() {
    const overlay = document.getElementById('modal-overlay');
    const closeBtn = document.getElementById('modal-close-btn');

    if (closeBtn) closeBtn.onclick = close;
    if (overlay) overlay.onclick = (e) => {
      if (e.target === overlay) close();
    };

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
    });
  }

  return { open, close, init };
})();

window.Modals = Modals;