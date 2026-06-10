const Waterfall = (canvasId) => {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext("2d");
  const cols = 128;
  let running = false;
  let imageData = null;

  const resize = () => {
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.max(400, rect.width || 800);
    canvas.height = rect.height || 150;
  };

  const colorFromValue = (v) => {
    if (v < 85) return `rgb(0, 0, ${Math.floor(v * 3)})`;
    if (v < 170) return `rgb(0, ${Math.floor((v - 85) * 3)}, 255)`;
    return `rgb(${Math.floor((v - 170) * 3)}, ${Math.floor(255 - (v - 170) * 3)}, 255)`;
  };

  let rafId = null;
  const update = () => {
    if (!running) return;
    const w = canvas.width, h = canvas.height;

    ctx.drawImage(canvas, 0, 0, w, h - 2, 0, 2, w, h - 2);
    ctx.globalCompositeOperation = 'source-over';

    const row = [];
    for (let i = 0; i < cols; i++) {
      const v = Math.random() * 255;
      row.push(v);
    }

    for (let i = 0; i < row.length; i++) {
      const v = row[i];
      ctx.fillStyle = colorFromValue(v);
      ctx.fillRect(i * (w / cols), 0, (w / cols) + 1, 2);
    }

    ctx.globalCompositeOperation = 'lighter';
    rafId = requestAnimationFrame(update);
  };

  const start = () => {
    if (running) return;
    running = true;
    resize();
    ctx.fillStyle = '#050810';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    update();
  };

  const stop = () => {
    running = false;
    if (rafId) cancelAnimationFrame(rafId);
  };

  return { start, stop, resize };
};

window.Waterfall = { Waterfall };