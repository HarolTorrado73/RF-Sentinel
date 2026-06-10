const Dashboard = (() => {
  const SIGNAL_TYPES = ['AM', 'FM', 'LSB', 'USB', 'CW', 'WFM', 'NFM', 'DATA'];
  const BASES = [433.92, 315.00, 868.30, 915.00, 1090.00, 121.50, 144.00, 433.00, 27.00];
  let signalCounter = 0;
  let detectedSignals = [];
  let activeFreq = 433.92;
  let signalStrength = -45;
  let snr = 18;
  let canvas = null;
  let ctx = null;
  let intensityHistory = [];
  const MAX_HISTORY = 100;

  function randomFreq() {
    const base = BASES[Math.floor(Math.random() * BASES.length)];
    return parseFloat((base + (Math.random() - 0.5) * 5).toFixed(4));
  }

  function randomType() {
    return SIGNAL_TYPES[Math.floor(Math.random() * SIGNAL_TYPES.length)];
  }

  function randomStrength() {
    return Math.round(-90 + Math.random() * 70);
  }

  function formatFreq(mhz) {
    return mhz.toFixed(3) + ' MHz';
  }

  function formatStrength(dbm) {
    return dbm + ' dBm';
  }

  function generateSignal() {
    return {
      freq: randomFreq(),
      type: randomType(),
      strength: randomStrength(),
      time: new Date().toISOString(),
      status: Math.random() > 0.15 ? 'ACTIVE' : 'IDLE'
    };
  }

  function updateSimulated() {
    activeFreq = parseFloat((activeFreq + (Math.random() - 0.5) * 0.2).toFixed(4));
    activeFreq = Math.max(27, Math.min(6000, activeFreq));

    signalStrength = Math.round(Math.max(-90, Math.min(-20, signalStrength + (Math.random() - 0.5) * 10));
    snr = Math.round(Math.max(0, Math.min(40, snr + (Math.random() - 0.5) * 4));

    if (Math.random() > 0.3) {
      const sig = generateSignal();
      detectedSignals.unshift(sig);
      signalCounter++;
      if (detectedSignals.length > 30) detectedSignals.pop();
    }

    if (ctx) {
      intensityHistory.push(signalStrength);
      if (intensityHistory.length > MAX_HISTORY) intensityHistory.shift();
    }
  }

  function renderMetrics() {
    const freqEl = document.getElementById('range-counter');
    const strengthEl = document.getElementById('strength-counter');
    const snrEl = document.getElementById('snr-counter');
    const actCountEl = document.getElementById('devices-counter');
    const sigCountEl = document.getElementById('signals-counter');

    if (freqEl) freqEl.textContent = formatFreq(activeFreq);
    if (strengthEl) strengthEl.textContent = formatStrength(signalStrength);
    if (snrEl) snrEl.textContent = snr + ' dB';
    if (sigCountEl) sigCountEl.textContent = signalCounter.toLocaleString();
    if (actCountEl) actCountEl.textContent = detectedSignals.length;
  }

  function renderLists() {
    const signalList = document.getElementById('signal-list');
    const activityLog = document.getElementById('activity-log');

    if (signalList && detectedSignals.length > 0) {
      signalList.innerHTML = detectedSignals.slice(0, 20).map(s => {
        const timeStr = new Date(s.time).toLocaleTimeString();
        return `<li class="signal-item">${formatFreq(s.freq)} | ${s.type} | ${formatStrength(s.strength)}</li>`;
      }).join('');
    }

    if (activityLog) {
      const msgs = ['Signal detected', 'Scan started', 'Export complete', 'Capture saved', 'Module loaded'];
      activityLog.innerHTML = msgs.slice(0, 5).map(m => {
        return `<li class="signal-item">${m}</li>`;
      }).join('');
    }
  }

  function drawChart() {
    if (!ctx || !canvas) return;
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    ctx.strokeStyle = '#0891b2';
    ctx.lineWidth = 2;
    ctx.beginPath();

    if (intensityHistory.length < 2) return;

    const minDb = -90;
    const maxDb = -20;
    const range = maxDb - minDb;
    const step = w / (MAX_HISTORY - 1);

    intensityHistory.forEach((db, i) => {
      const x = i * step;
      const y = h - ((db - minDb) / range) * h;
      const cy = Math.max(0, Math.min(h, y));
      if (i === 0) ctx.moveTo(x, cy);
      else ctx.lineTo(x, cy);
    });

    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.strokeStyle = '#0a1628';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, h / 2);
    ctx.lineTo(w, h / 2);
    ctx.stroke();
  }

  function initChart() {
    canvas = document.getElementById('spectrum-canvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.max(400, rect.width || 800);
    canvas.height = 160;
  }

  function updateLoop() {
    updateSimulated();
    renderMetrics();
    drawChart();
    if (Math.random() > 0.4) renderLists();
  }

  function startPolling() {
    updateLoop();
    setInterval(updateLoop, 500);
  }

  function initDashboard() {
    initChart();
    renderLists();
    startPolling();
  }

  return {
    initDashboard,
    updateMetrics: () => ({ freq: activeFreq, signalStrength, snr, count: signalCounter }),
    getDetectedSignals: () => [...detectedSignals]
  };
})();

window.Dashboard = Dashboard;