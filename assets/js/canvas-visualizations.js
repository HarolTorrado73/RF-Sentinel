function ParticleSystem(canvasId) {
  this.canvas = document.getElementById(canvasId);
  if (!this.canvas) return;
  this.ctx = this.canvas.getContext("2d");
  this.particles = [];
  this.particleCount = 60;
  this.connectionDistance = 120;
  this.resize();
  this.init();
  new ResizeObserver(() => this.resize()).observe(this.canvas);
}

ParticleSystem.prototype.resize = function () {
   this.canvas.width = window.innerWidth;
   this.canvas.height = window.innerHeight;
};

ParticleSystem.prototype.init = function () {
  for (let i = 0; i < this.particleCount; i++) {
    this.particles.push({
      x: Math.random() * this.canvas.width,
      y: Math.random() * this.canvas.height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      size: Math.random() * 1.5 + 0.5,
    });
  }
};

ParticleSystem.prototype.update = function () {
  const ctx = this.ctx;
  const w = this.canvas.width;
  const h = this.canvas.height;
  ctx.clearRect(0, 0, w, h);

  for (let p of this.particles) {
    p.x += p.vx;
    p.y += p.vy;
    if (p.x < 0) p.x = w;
    if (p.x > w) p.x = 0;
    if (p.y < 0) p.y = h;
    if (p.y > h) p.y = 0;

    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(0,212,255,0.6)";
    ctx.fill();
  }

  for (let i = 0; i < this.particles.length; i++) {
    for (let j = i + 1; j < this.particles.length; j++) {
      const dx = this.particles[i].x - this.particles[j].x;
      const dy = this.particles[i].y - this.particles[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < this.connectionDistance) {
        ctx.beginPath();
        ctx.moveTo(this.particles[i].x, this.particles[i].y);
        ctx.lineTo(this.particles[j].x, this.particles[j].y);
        ctx.strokeStyle = `rgba(0,212,255,${0.15 * (1 - dist / this.connectionDistance)})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }
};

ParticleSystem.prototype.start = function () {
  const loop = () => {
    this.update();
    this.rafId = requestAnimationFrame(loop);
  };
  loop();
};

ParticleSystem.prototype.stop = function () {
  cancelAnimationFrame(this.rafId);
};

function RFBackgroundAnimation(canvasId) {
   this.canvas = document.getElementById(canvasId);
   if (!this.canvas) return;
   this.ctx = this.canvas.getContext("2d");
   this.waves = [];
   this.maxWaves = 8;
   this.resize();
   this.init();
   window.addEventListener('resize', () => this.resize());
  }

  RFBackgroundAnimation.prototype.resize = function () {
   this.canvas.width = window.innerWidth;
   this.canvas.height = window.innerHeight;
  };

RFBackgroundAnimation.prototype.init = function () {
  for (let i = 0; i < this.maxWaves; i++) {
    this.waves.push({
      radius: 0,
      maxRadius: Math.max(this.canvas.width, this.canvas.height) * 0.6,
      speed: 0.3 + i * 0.1,
      opacity: 0,
    });
  }
};

RFBackgroundAnimation.prototype.update = function () {
  const ctx = this.ctx;
  const cx = this.canvas.width / 2;
  const cy = this.canvas.height / 2;
  ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

  for (let w of this.waves) {
    w.radius += w.speed;
    if (w.radius > w.maxRadius) {
      w.radius = 0;
      w.opacity = 0.25;
    }
    const progress = w.radius / w.maxRadius;
    const alpha = 0.25 * (1 - progress);
    ctx.beginPath();
    ctx.arc(cx, cy, w.radius, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(0,212,255,${alpha})`;
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }
};

RFBackgroundAnimation.prototype.start = function () {
  const loop = () => {
    this.update();
    this.rafId = requestAnimationFrame(loop);
  };
  loop();
};

RFBackgroundAnimation.prototype.stop = function () {
  cancelAnimationFrame(this.rafId);
};

function SpectrumAnalyzer(canvasId) {
  this.canvas = document.getElementById(canvasId);
  if (!this.canvas) return;
  this.ctx = this.canvas.getContext("2d");
  this.barCount = 64;
  this.bars = [];
  this.resize();
  this.init();
  new ResizeObserver(() => this.resize()).observe(this.canvas);
}

SpectrumAnalyzer.prototype.resize = function () {
   const parent = this.canvas.parentElement;
   const rect = parent.getBoundingClientRect();
   this.canvas.width = rect.width || parent.clientWidth || 800;
   this.canvas.height = rect.height || parent.clientHeight || 160;
   this.barWidth = this.canvas.width / this.barCount;
};

SpectrumAnalyzer.prototype.init = function () {
  for (let i = 0; i < this.barCount; i++) {
    this.bars.push({
      value: 0.1 + Math.random() * 0.2,
      target: Math.random(),
      speed: 0.01 + Math.random() * 0.03,
    });
  }
};

SpectrumAnalyzer.prototype.update = function () {
  const ctx = this.ctx;
  const w = this.canvas.width;
  const h = this.canvas.height;
  ctx.clearRect(0, 0, w, h);

  for (let i = 0; i < this.barCount; i++) {
    const bar = this.bars[i];
    bar.target += (Math.random() - 0.5) * 0.1;
    bar.target = Math.max(0.05, Math.min(1, bar.target));
    bar.value += (bar.target - bar.value) * bar.speed;
    const barH = bar.value * h * 0.8;
    const x = i * this.barWidth;
    const gradient = ctx.createLinearGradient(0, h, 0, h - barH);
    gradient.addColorStop(0, "#00d4ff");
    gradient.addColorStop(0.5, "#3b82f6");
    gradient.addColorStop(1, "#8b5cf6");
    ctx.fillStyle = gradient;
    ctx.fillRect(x + 1, h - barH, this.barWidth - 2, barH);
  }
};

SpectrumAnalyzer.prototype.start = function () {
  const loop = () => {
    this.update();
    this.rafId = requestAnimationFrame(loop);
  };
  loop();
};

SpectrumAnalyzer.prototype.stop = function () {
  cancelAnimationFrame(this.rafId);
};

function Waterfall(canvasId) {
  this.canvas = document.getElementById(canvasId);
  if (!this.canvas) return;
  this.ctx = this.canvas.getContext("2d");
  this.cols = 128;
  this.scrollY = 0;
  this.data = [];
  this.resize();
  this.initData();
  new ResizeObserver(() => this.resize()).observe(this.canvas);
}

Waterfall.prototype.resize = function () {
   const parent = this.canvas.parentElement;
   const rect = parent.getBoundingClientRect();
   this.canvas.width = rect.width || parent.clientWidth || 800;
   this.canvas.height = rect.height || parent.clientHeight || 120;
   this.cellW = this.canvas.width / this.cols;
   this.cellH = 2;
};

Waterfall.prototype.initData = function () {
  const rows = Math.ceil(this.canvas.height / this.cellH);
  for (let r = 0; r < rows; r++) {
    const row = [];
    for (let c = 0; c < this.cols; c++) {
      row.push(Math.random());
    }
    this.data.push(row);
  }
};

Waterfall.prototype.generateRow = function () {
  const row = [];
  for (let i = 0; i < this.cols; i++) {
    const val = Math.random();
    row.push(val > 0.94 ? 1 : val > 0.7 ? val * 0.5 + 0.4 : Math.random() * 0.25);
  }
  return row;
};

Waterfall.prototype.colorFromValue = function (v) {
  if (v < 0.33) return `rgb(0,0,${Math.floor(v * 3 * 180)})`;
  if (v < 0.66) return `rgb(0,${Math.floor((v - 0.33) * 3 * 212)},${Math.floor(255 - (v - 0.33) * 3 * 180)})`;
  return `rgb(${Math.floor((v - 0.66) * 3 * 139)},${Math.floor(212 - (v - 0.66) * 3 * 100)},255)`;
};

Waterfall.prototype.update = function () {
  const ctx = this.ctx;
  const h = this.canvas.height;
  const rows = this.data.length;
  if (rows > 0) {
    ctx.drawImage(this.canvas, 0, 0, this.canvas.width, h - this.cellH, 0, this.cellH, this.canvas.width, h - this.cellH);
  }
  const newRow = this.generateRow();
  for (let c = 0; c < this.cols; c++) {
    ctx.fillStyle = this.colorFromValue(newRow[c]);
    ctx.fillRect(c * this.cellW, 0, this.cellW + 1, this.cellH);
  }
};

Waterfall.prototype.start = function () {
  const loop = () => {
    this.update();
    this.rafId = requestAnimationFrame(loop);
  };
  loop();
};

Waterfall.prototype.stop = function () {
  cancelAnimationFrame(this.rafId);
};

function ActivityFeed(canvasId) {
  this.canvas = document.getElementById(canvasId);
  if (!this.canvas) return;
  this.ctx = this.canvas.getContext("2d");
  this.lines = [];
  this.maxLines = 8;
  this.resize();
  this.seed();
  new ResizeObserver(() => this.resize()).observe(this.canvas);
}

ActivityFeed.prototype.resize = function () {
  this.canvas.width = this.canvas.parentElement.clientWidth;
  this.canvas.height = this.canvas.parentElement.clientHeight;
  this.lineHeight = this.canvas.height / this.maxLines;
};

ActivityFeed.prototype.seed = function () {
  const signals = [
    "GSM 850 -97dBm detected",
    "LTE Band 3 -89dBm signal",
    "LoRa 433MHz RSSI -78dBm",
    "FM 106.5MHz -62dBm carrier",
    "ZigBee CH11 -91dBm",
    "4G LTE B7 -84dBm active",
    "RF spurious 2.4GHz detected",
    "Bluetooth LE adv detected",
    "WiFi 2.4GHz AP beacon",
    "Unknown burst 915MHz",
  ];
  for (let i = 0; i < this.maxLines; i++) {
    this.lines.push({
      text: signals[Math.floor(Math.random() * signals.length)],
      offset: i * this.lineHeight,
      fade: 1,
    });
  }
};

ActivityFeed.prototype.update = function () {
  const ctx = this.ctx;
  const w = this.canvas.width;
  ctx.clearRect(0, 0, w, this.canvas.height);
  ctx.font = "11px monospace";

  for (let i = this.lines.length - 1; i >= 0; i--) {
    const line = this.lines[i];
    line.offset -= 0.5;
    if (line.offset < -this.lineHeight) {
      line.offset = this.canvas.height;
      const signals = [
        "GSM 850 -97dBm detected",
        "LTE Band 3 -89dBm signal",
        "LoRa 433MHz RSSI -78dBm",
        "FM 106.5MHz -62dBm carrier",
        "ZigBee CH11 -91dBm",
        "4G LTE B7 -84dBm active",
        "RF spurious 2.4GHz detected",
        "Bluetooth LE adv detected",
        "WiFi 2.4GHz AP beacon",
        "Unknown burst 915MHz",
      ];
      line.text = signals[Math.floor(Math.random() * signals.length)];
    }
    const y = line.offset;
    if (y < 0 || y > this.canvas.height) continue;
    const alpha = Math.min(1, y / 20, (this.canvas.height - y) / 20, 1);
    ctx.fillStyle = `rgba(0,212,255,${alpha * 0.9})`;
    ctx.fillText(line.text, 12, y);
  }
};

ActivityFeed.prototype.start = function () {
  const loop = () => {
    this.update();
    this.rafId = requestAnimationFrame(loop);
  };
  loop();
};

ActivityFeed.prototype.stop = function () {
  cancelAnimationFrame(this.rafId);
};

function SignalDetectionFeed(canvasId) {
  this.canvas = document.getElementById(canvasId);
  if (!this.canvas) return;
  this.ctx = this.canvas.getContext("2d");
  this.detections = [];
  this.maxDetections = 6;
  this.tick = 0;
  this.resize();
  this.seed();
  new ResizeObserver(() => this.resize()).observe(this.canvas);
}

SignalDetectionFeed.prototype.resize = function () {
  this.canvas.width = this.canvas.parentElement.clientWidth;
  this.canvas.height = this.canvas.parentElement.clientHeight;
  this.rowHeight = this.canvas.height / this.maxDetections;
};

SignalDetectionFeed.prototype.seed = function () {
  for (let i = 0; i < this.maxDetections; i++) {
    this.detections.push(this.newDetection());
  }
};

SignalDetectionFeed.prototype.newDetection = function () {
  const now = new Date();
  const ts =
    now.getHours().toString().padStart(2, "0") +
    ":" +
    now.getMinutes().toString().padStart(2, "0") +
    ":" +
    now.getSeconds().toString().padStart(2, "0");
  return {
    ts: ts,
    freq: (100 + Math.random() * 2400).toFixed(1) + " MHz",
    rssi: (-40 - Math.random() * 60).toFixed(0) + " dBm",
    protocol: ["GSM", "LTE", "LoRa", "WiFi", "BT", "ZigBee"][Math.floor(Math.random() * 6)],
    y: this.canvas.height,
  };
};

SignalDetectionFeed.prototype.update = function () {
  const ctx = this.ctx;
  const w = this.canvas.width;
  ctx.clearRect(0, 0, w, this.canvas.height);
  ctx.font = "12px monospace";

  for (let i = this.detections.length - 1; i >= 0; i--) {
    const d = this.detections[i];
    d.y -= 0.4;
    if (d.y < -this.rowHeight) {
      this.detections[i] = this.newDetection();
      continue;
    }
    const y = d.y;
    const alpha = Math.min(1, (y + this.rowHeight) / 30, (this.canvas.height - y) / 30);
    ctx.fillStyle = `rgba(139,92,246,${alpha})`;
    ctx.fillText(d.ts, 12, y + 14);
    ctx.fillStyle = `rgba(0,212,255,${alpha})`;
    ctx.fillText(d.freq, 100, y + 14);
    ctx.fillStyle = `rgba(59,130,246,${alpha})`;
    ctx.fillText(d.rssi, 240, y + 14);
    ctx.fillStyle = `rgba(139,92,246,${alpha * 0.8})`;
    ctx.fillText(d.protocol, 340, y + 14);
    ctx.strokeStyle = `rgba(0,212,255,${alpha * 0.15})`;
    ctx.beginPath();
    ctx.moveTo(0, y + 24);
    ctx.lineTo(w, y + 24);
    ctx.stroke();
  }
};

SignalDetectionFeed.prototype.start = function () {
  const loop = () => {
    this.update();
    this.rafId = requestAnimationFrame(loop);
  };
  loop();
};

SignalDetectionFeed.prototype.stop = function () {
  cancelAnimationFrame(this.rafId);
};

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    ParticleSystem,
    RFBackgroundAnimation,
    SpectrumAnalyzer,
    Waterfall,
    ActivityFeed,
    SignalDetectionFeed,
  };
}
