const SpectrumAnalyzer = (canvasId) => {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext("2d");
  let barCount = 128;

  const resize = () => {
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.max(400, rect.width || 800);
    canvas.height = rect.height || 200;
    barCount = canvas.width / 8;
  };

  let running = false;
  let rafId = null;

  const update = () => {
    if (!running) return;
    const w = canvas.width, h = canvas.height;
    ctx.fillStyle = 'rgba(6,10,20,0.2)';
    ctx.fillRect(0, 0, w, h);

    for (let i = 0; i < barCount; i++) {
      const barH = Math.random() * h * 0.7 + h * 0.1;
      const x = i * (w / barCount);
      const gradient = ctx.createLinearGradient(0, h, 0, h - barH);
      gradient.addColorStop(0, "#00f3ff");
      gradient.addColorStop(1, "#0077ff");
      ctx.fillStyle = gradient;
      ctx.fillRect(x, h - barH, (w / barCount) - 1, barH);
    }

    rafId = requestAnimationFrame(update);
  };

  const start = () => {
    if (running) return;
    running = true;
    resize();
    update();
  };

  const stop = () => {
    running = false;
  };

  return { start, stop, resize };
};

window.Spectrum = { SpectrumAnalyzer };