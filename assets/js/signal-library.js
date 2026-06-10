const SIGNALS = [
  {
    id: "433mhz",
    name: "433 MHz",
    description: "Usado en controles remotos, sensores inalámbricos y sistemas de automatización doméstica.",
    color: "#4fc3f7",
    preview: "ask-ook",
    characteristics: [
      { label: "Frecuencia", value: "433.92 MHz" },
      { label: "Modulación", value: "ASK / OOK" },
      { label: "Ancho de banda", value: "~300 kHz" },
      { label: "Potencia típica", value: "10 mW" },
      { label: "Rango", value: "hasta 100 m" },
    ],
    draw(ctx, w, h) {
      const t = Date.now() / 1000;
      ctx.strokeStyle = this.color;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      const centerY = h / 2;
      const samples = 400;
      for (let i = 0; i < samples; i++) {
        const x = (i / samples) * w;
        const f = 440;
        const pos = (Math.floor(i / 8) % 2 === 0 ? 0 : 1) * Math.sin((i / samples) * Math.PI * 4) * 0.4;
        const val = centerY + Math.sin(i / samples * Math.PI * f + t) * (h * 0.25) * (i / samples > 0.6 ? pos : pos * 0.3);
        i === 0 ? ctx.moveTo(x, val) : ctx.lineTo(x, val);
      }
      ctx.stroke();
    },
  },
  {
    id: "315mhz",
    name: "315 MHz",
    description: "Utilizado en alarmas de auto, controles de garaje y sistemas de acceso vehicular.",
    color: "#81c784",
    preview: "ask-ook",
    characteristics: [
      { label: "Frecuencia", value: "315 MHz" },
      { label: "Modulación", value: "ASK" },
      { label: "Ancho de banda", value: "~300 kHz" },
      { label: "Códigos", value: "Rolling / Hopping" },
      { label: "Alcance", value: "50-150 m" },
    ],
    draw(ctx, w, h) {
      const t = Date.now() / 1000;
      ctx.strokeStyle = this.color;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      const centerY = h / 2;
      const samples = 400;
      const freq = 370;
      for (let i = 0; i < samples; i++) {
        const x = (i / samples) * w;
        const hopping = Math.sin(i / samples * Math.PI * 6) > 0 ? 0.5 : 1;
        const val = centerY + Math.sin(i / samples * Math.PI * freq + t * 2.5) * (h * 0.22) * hopping;
        i === 0 ? ctx.moveTo(x, val) : ctx.lineTo(x, val);
      }
      ctx.stroke();
    },
  },
  {
    id: "adsb",
    name: "ADS-B",
    description: "Datos de aviación automática: posición, velocidad e identificación de aeronaves en vuelo.",
    color: "#ffd54f",
    preview: "burst",
    characteristics: [
      { label: "Frecuencia", value: "1090 MHz" },
      { label: "Modulación", value: "Mode S" },
      { label: "Ancho de banda", value: "2 MHz" },
      { label: "Longitud mensaje", value: "56-112 bits" },
      { label: "Tasa bits", value: "1 Mbps" },
    ],
    draw(ctx, w, h) {
      const t = Date.now() / 1000;
      ctx.fillStyle = this.color;
      const burstLen = 60;
      const gap = 160;
      const period = burstLen + gap;
      const xOffset = (t * 30) % period;
      const burstX = w * 0.35 + xOffset;
      ctx.fillRect(burstX, h * 0.15, burstLen, h * 0.7);
      ctx.fillRect(Math.max(0, burstX - period), h * 0.15, burstLen, h * 0.7);
      const xAxis = h * 0.85;
      ctx.strokeStyle = "rgba(255,255,255,0.3)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, xAxis);
      ctx.lineTo(w, xAxis);
      ctx.stroke();
    },
  },
  {
    id: "fm",
    name: "FM Broadcast",
    description: "Radio FM comercial. Banda ancha con portadora modulada en frecuencia y espaciado de 200 kHz.",
    color: "#e57373",
    preview: "wideband",
    characteristics: [
      { label: "Banda", value: "87.5 - 108 MHz" },
      { label: "Modulación", value: "FM Wideband" },
      { label: "Espaciado", value: "200 kHz" },
      { label: "Potencia", value: "hasta 100 kW" },
      { label: "Desviación", value: "±75 kHz" },
    ],
    draw(ctx, w, h) {
      const t = Date.now() / 1000;
      const gradients = [
        { color: this.color, freq: 8, amp: 0.18, phase: 0 },
        { color: "#ffab91", freq: 11.5, amp: 0.12, phase: 1.2 },
        { color: "#ffcc80", freq: 16, amp: 0.08, phase: 2.1 },
      ];
      gradients.forEach((g) => {
        ctx.strokeStyle = g.color;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        const centerY = h / 2;
        const samples = 500;
        for (let i = 0; i < samples; i++) {
          const x = (i / samples) * w;
          const val = centerY + Math.sin(i / samples * Math.PI * g.freq + t + g.phase) * (h * g.amp);
          i === 0 ? ctx.moveTo(x, val) : ctx.lineTo(x, val);
        }
        ctx.stroke();
      });
    },
  },
  {
    id: "weather",
    name: "Weather Stations",
    description: "Sensores meteorológicos inalámbricos que transmiten datos de temperatura, humedad y presión.",
    color: "#ba68c8",
    preview: "burst",
    characteristics: [
      { label: "Bandas", value: "433 / 868 MHz" },
      { label: "Protocolos", value: "Acurite, Oregon, Fine Offset" },
      { label: "Modulación", value: "ASK / FSK" },
      { label: "Intervalo", value: "30-60 s" },
      { label: "Duración trama", value: "~10 ms" },
    ],
    draw(ctx, w, h) {
      const t = Date.now() / 1000;
      const period = 2;
      const elapsed = t % period;
      const barW = 8;
      const gap = 30;
      const cols = Math.floor(w / (barW + gap));
      const rows = 2;
      const rowH = h / rows;
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const x = c * (barW + gap);
          const yBase = r * rowH + rowH * 0.15;
          const rowPhase = r * 0.7;
          const burstStart = ((c * 0.2 + rowPhase) % period);
          const burstEnd = burstStart + 0.18;
          const active = elapsed >= burstStart && elapsed < burstEnd;
          ctx.fillStyle = active ? this.color : `${this.color}22`;
          const barH = active ? rowH * 0.65 : rowH * 0.12;
          ctx.fillRect(x, yBase + rowH * 0.15 - active ? 0 : 0, barW, barH);
        }
      }
    },
},
];

function initSignalLibrary(containerId) {
  const container = typeof containerId === "string" ? document.getElementById(containerId) : containerId;
  if (!container) return;
  renderSignalCards(container);
}

function renderSignalCards(container) {
  container.innerHTML = SIGNALS.map((signal) => `
    <div class="signal-card" data-section-id="${signal.id}">
      <div class="signal-header">
        <span class="signal-badge" style="background:${signal.color}">${signal.name}</span>
        <h3>${signal.name}</h3>
        <p class="signal-desc">${signal.description}</p>
      </div>
      <div class="signal-preview">
        <canvas id="canvas-${signal.id}" width="360" height="140"></canvas>
      </div>
      <table class="signal-table">
        <thead>
          <tr>
            <th>Característica</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          ${signal.characteristics.map((c) => `
            <tr>
              <td>${c.label}</td>
              <td>${c.value}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `).join("");

  SIGNALS.forEach((signal) => {
    startSignalPreview(signal);
  });
}

function startSignalPreview(signal) {
  const canvas = document.getElementById(`canvas-${signal.id}`);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  function frame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "rgba(10,14,26,0.95)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    signal.draw(ctx, canvas.width, canvas.height);
    requestAnimationFrame(frame);
  }
  frame();
}

window.signalLibrary = { initSignalLibrary };
