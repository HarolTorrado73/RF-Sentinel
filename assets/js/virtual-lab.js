const virtualLab = (() => {
  let specCanvas, specCtx, specRunning = false;
  let wfCanvas, wfCtx, wfRunning = false;
  let scanRunning = false;
  let scanProgress = 0;

  function init(spectrumId, waterfallId) {
    specCanvas = document.getElementById(spectrumId);
    specCtx = specCanvas ? specCanvas.getContext('2d') : null;
    wfCanvas = document.getElementById(waterfallId);
    wfCtx = wfCanvas ? wfCanvas.getContext('2d') : null;

    if (specCtx) resizeCanvas(specCanvas);
    if (wfCtx) resizeCanvas(wfCanvas);

    new ResizeObserver(() => {
      if (specCanvas) resizeCanvas(specCanvas);
      if (wfCanvas) resizeCanvas(wfCanvas);
    }).observe(document.body);
  }

function resizeCanvas(c) {
     const parent = c.parentElement;
     if (parent) {
       const rect = parent.getBoundingClientRect();
       c.width = Math.max(300, rect.width || 600);
       c.height = rect.height || 160;
     }
   }

  function drawSpectrum() {
    if (!specCtx || !specRunning) return;
    const w = specCanvas.width, h = specCanvas.height;
    specCtx.fillStyle = 'rgba(6,10,20,0.3)';
    specCtx.fillRect(0, 0, w, h);

    const signals = [
      { center: w * 0.2, width: w * 0.08, height: 0.7 },
      { center: w * 0.4, width: w * 0.05, height: 0.55 },
      { center: w * 0.6, width: w * 0.12, height: 0.85 },
      { center: w * 0.75, width: w * 0.06, height: 0.45 },
      { center: w * 0.88, width: w * 0.1, height: 0.65 },
    ];

    for (const sig of signals) {
      const grad = specCtx.createLinearGradient(sig.center - sig.width / 2, h, sig.center + sig.width / 2, h);
      grad.addColorStop(0, 'rgba(0,212,255,0)');
      grad.addColorStop(0.5, 'rgba(0,212,255,0.9)');
      grad.addColorStop(1, 'rgba(0,212,255,0)');
      specCtx.fillStyle = grad;
      specCtx.fillRect(sig.center - sig.width / 2, h * (1 - sig.height * 0.8), sig.width, h * sig.height * 0.8);

      specCtx.beginPath();
      specCtx.moveTo(sig.center - sig.width / 2, h * (1 - sig.height * 0.8));
      specCtx.lineTo(sig.center, h * (1 - sig.height));
      specCtx.lineTo(sig.center + sig.width / 2, h * (1 - sig.height * 0.8));
      specCtx.strokeStyle = '#00d4ff';
      specCtx.lineWidth = 1.5;
      specCtx.stroke();
    }

    requestAnimationFrame(() => drawSpectrum());
  }

  let wfOffset = 0;
  function drawWaterfall() {
    if (!wfCtx || !wfRunning) return;
    const w = wfCanvas.width, h = wfCanvas.height;
    const imageData = wfCtx.createImageData(w, 1);

    for (let x = 0; x < w; x++) {
      const r = x / w;
      const noise = Math.random() * 15;
      const sig1 = r > 0.18 && r < 0.25 ? 120 : 0;
      const sig2 = r > 0.38 && r < 0.43 ? 100 : 0;
      const sig3 = r > 0.55 && r < 0.68 ? 150 : 0;
      const val = Math.min(255, noise + sig1 + sig2 + sig3);

      const idx = x * 4;
      imageData.data[idx] = val * 0.1;
      imageData.data[idx + 1] = val * 0.5;
      imageData.data[idx + 2] = val;
      imageData.data[idx + 3] = 255;
    }

    wfCtx.drawImage(wfCanvas, 0, 0, w, h - 1, 0, 1, w, h - 1);
    wfCtx.putImageData(imageData, 0, 0);

    requestAnimationFrame(() => drawWaterfall());
  }

  function startSpectrum() {
    if (!specCanvas || specRunning) return;
    specRunning = true;
    resizeCanvas(specCanvas);
    drawSpectrum();
  }

  function stopSpectrum() {
    specRunning = false;
  }

  function startWaterfall() {
    if (!wfCanvas || wfRunning) return;
    wfRunning = true;
    wfCtx.fillStyle = '#060a14';
    wfCtx.fillRect(0, 0, wfCanvas.width, wfCanvas.height);
    drawWaterfall();
  }

  function stopWaterfall() {
    wfRunning = false;
  }

  function startScan() {
    if (scanRunning) return;
    scanRunning = true;
    scanProgress = 0;
    animateScan();
  }

  function stopScan() {
    scanRunning = false;
    scanProgress = 0;
    const bar = document.getElementById('scan-progress-bar');
    const label = document.getElementById('scan-progress-text');
    if (bar) bar.style.width = '0%';
    if (label) label.textContent = '0%';
  }

  function animateScan() {
    if (!scanRunning) return;
    scanProgress += 2;
    if (scanProgress > 100) scanProgress = 100;

    const bar = document.getElementById('scan-progress-bar');
    const label = document.getElementById('scan-progress-text');
    if (bar) bar.style.width = scanProgress + '%';
    if (label) label.textContent = scanProgress + '%';

    if (scanProgress < 100) {
      setTimeout(() => requestAnimationFrame(animateScan), 80);
    } else {
      scanRunning = false;
      if (label) label.textContent = 'Complete';
    }
  }

  return { init, startSpectrum, stopSpectrum, startWaterfall, stopWaterfall, startScan, stopScan };
})();
