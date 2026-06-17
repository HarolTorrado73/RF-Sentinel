const Dashboard = (() => {
  const SIGNAL_TYPES = ['AM', 'FM', 'LSB', 'USB', 'CW', 'WFM', 'NFM', 'DATA'];
  const BASES = [433.92, 315.00, 868.30, 915.00, 1090.00, 121.50, 144.00, 433.00, 27.00];
  let signalCounter = 0;
  let detectedSignals = [];
  let activeFreq = 433.92;
  let signalStrength = -45;
  let snr = 18;

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

    signalStrength = Math.round(Math.max(-90, Math.min(-20, signalStrength + (Math.random() - 0.5) * 10)));
    snr = Math.round(Math.max(0, Math.min(40, snr + (Math.random() - 0.5) * 4));

    if (Math.random() > 0.3) {
      const sig = generateSignal();
      detectedSignals.unshift(sig);
      signalCounter++;
      if (detectedSignals.length > 30) detectedSignals.pop();
    }
  }

  function renderMetrics() {
    const freqEl = document.getElementById('range-counter');
    const devicesEl = document.getElementById('devices-counter');
    const sigCountEl = document.getElementById('signals-counter');
    const exportsEl = document.getElementById('exports-counter');

    if (freqEl) freqEl.textContent = formatFreq(activeFreq);
    if (devicesEl) devicesEl.textContent = detectedSignals.length;
    if (sigCountEl) sigCountEl.textContent = signalCounter.toLocaleString();
    if (exportsEl) exportsEl.textContent = '89';
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

  function updateLoop() {
    updateSimulated();
    renderMetrics();
    renderLists();
  }

  function startPolling() {
    updateLoop();
    setInterval(updateLoop, 500);
  }

  function initDashboard() {
    renderLists();
    startPolling();
  }

  return {
    initDashboard,
    updateMetrics: () => ({ freq: activeFreq, signalStrength, snr, count: signalCounter }),
    getDetectedSignals: () => [...detectedSignals]
  };
})();
