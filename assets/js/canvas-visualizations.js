const CanvasVisualizations = (() => {
  function ParticleSystem(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext("2d");
    let particles = [];
    let rafId = null;
    let resizeObserver = null;
    let intersectionObserver = null;
    let isVisible = true;

    const PARTICLE_COUNT = 60;
    const CONNECTION_DISTANCE = 120;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const init = () => {
      particles = [];
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.4,
          vy: (Math.random() - 0.5) * 0.4,
          size: Math.random() * 1.5 + 0.5,
        });
      }
    };

    const update = () => {
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      for (const p of particles) {
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

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < CONNECTION_DISTANCE) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(0,212,255,${0.15 * (1 - dist / CONNECTION_DISTANCE)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }
    };

    const loop = () => {
      if (!isVisible) return;
      update();
      rafId = requestAnimationFrame(loop);
    };

    const start = () => {
      if (rafId) return;
      loop();
    };

    const stop = () => {
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
    };

    const onVisibilityChange = (entries) => {
      const entry = entries[0];
      isVisible = entry.isIntersecting;
      if (isVisible && !rafId) {
        loop();
      } else if (!isVisible && rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
    };

    const destroy = () => {
      stop();
      if (resizeObserver) {
        resizeObserver.disconnect();
        resizeObserver = null;
      }
      if (intersectionObserver) {
        intersectionObserver.disconnect();
        intersectionObserver = null;
      }
    };

    const setupObservers = () => {
      resizeObserver = new ResizeObserver(() => resize());
      resizeObserver.observe(canvas);

      intersectionObserver = new IntersectionObserver(onVisibilityChange, { threshold: 0.1 });
      intersectionObserver.observe(canvas);
    };

    resize();
    init();
    setupObservers();
    start();

    return { start, stop, destroy };
  }

  function SpectrumAnalyzer(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext("2d");
    let bars = [];
    let rafId = null;
    let resizeObserver = null;
    let intersectionObserver = null;
    let isVisible = true;
    const BAR_COUNT = 64;

    const resize = () => {
      const parent = canvas.parentElement;
      const rect = parent.getBoundingClientRect();
      canvas.width = rect.width || parent.clientWidth || 800;
      canvas.height = rect.height || parent.clientHeight || 160;
    };

    const init = () => {
      bars = [];
      for (let i = 0; i < BAR_COUNT; i++) {
        bars.push({
          value: 0.1 + Math.random() * 0.2,
          target: Math.random(),
          speed: 0.01 + Math.random() * 0.03,
        });
      }
    };

    const update = () => {
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      for (let i = 0; i < BAR_COUNT; i++) {
        const bar = bars[i];
        bar.target += (Math.random() - 0.5) * 0.1;
        bar.target = Math.max(0.05, Math.min(1, bar.target));
        bar.value += (bar.target - bar.value) * bar.speed;
        const barH = bar.value * h * 0.8;
        const x = i * (w / BAR_COUNT);
        const gradient = ctx.createLinearGradient(0, h, 0, h - barH);
        gradient.addColorStop(0, "#00f3ff");
        gradient.addColorStop(0.5, "#3b82f6");
        gradient.addColorStop(1, "#8b5cf6");
        ctx.fillStyle = gradient;
        ctx.fillRect(x + 1, h - barH, (w / BAR_COUNT) - 2, barH);
      }
    };

    const loop = () => {
      if (!isVisible) return;
      update();
      rafId = requestAnimationFrame(loop);
    };

    const start = () => {
      if (rafId) return;
      loop();
    };

    const stop = () => {
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
    };

    const onVisibilityChange = (entries) => {
      const entry = entries[0];
      isVisible = entry.isIntersecting;
      if (isVisible && !rafId) {
        loop();
      } else if (!isVisible && rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
    };

    const destroy = () => {
      stop();
      if (resizeObserver) {
        resizeObserver.disconnect();
        resizeObserver = null;
      }
      if (intersectionObserver) {
        intersectionObserver.disconnect();
        intersectionObserver = null;
      }
    };

    const setupObservers = () => {
      resizeObserver = new ResizeObserver(() => resize());
      resizeObserver.observe(canvas);

      intersectionObserver = new IntersectionObserver(onVisibilityChange, { threshold: 0.1 });
      intersectionObserver.observe(canvas);
    };

    resize();
    init();
    setupObservers();
    start();

    return { start, stop, destroy };
  }

  function WaterfallRenderer(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext("2d");
    const COLS = 128;
    let rafId = null;
    let resizeObserver = null;
    let intersectionObserver = null;
    let isVisible = true;

    const resize = () => {
      const parent = canvas.parentElement;
      const rect = parent.getBoundingClientRect();
      canvas.width = rect.width || parent.clientWidth || 800;
      canvas.height = rect.height || parent.clientHeight || 160;
    };

    const colorFromValue = (v) => {
      if (v < 0.33) return `rgb(0,0,${Math.floor(v * 3 * 180)})`;
      if (v < 0.66) return `rgb(0,${Math.floor((v - 0.33) * 3 * 212)},${Math.floor(255 - (v - 0.33) * 3 * 180)})`;
      return `rgb(${Math.floor((v - 0.66) * 3 * 139)},${Math.floor(212 - (v - 0.66) * 3 * 100)},255)`;
    };

    const generateRow = () => {
      const row = [];
      for (let i = 0; i < COLS; i++) {
        const val = Math.random();
        row.push(val > 0.94 ? 1 : val > 0.7 ? val * 0.5 + 0.4 : Math.random() * 0.25);
      }
      return row;
    };

    const update = () => {
      const w = canvas.width;
      const h = canvas.height;
      const cellH = 2;
      const cellW = w / COLS;

      ctx.drawImage(canvas, 0, 0, w, h - cellH, 0, cellH, w, h - cellH);

      const newRow = generateRow();
      for (let c = 0; c < COLS; c++) {
        ctx.fillStyle = colorFromValue(newRow[c]);
        ctx.fillRect(c * cellW, 0, cellW + 1, cellH);
      }
    };

    const loop = () => {
      if (!isVisible) return;
      update();
      rafId = requestAnimationFrame(loop);
    };

    const start = () => {
      if (rafId) return;
      ctx.fillStyle = '#050810';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      loop();
    };

    const stop = () => {
      if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
    };

    const onVisibilityChange = (entries) => {
      const entry = entries[0];
      isVisible = entry.isIntersecting;
      if (isVisible && !rafId) {
        loop();
      } else if (!isVisible && rafId) {
        cancelAnimationFrame(rafId);
        rafId = null;
      }
    };

    const destroy = () => {
      stop();
      if (resizeObserver) {
        resizeObserver.disconnect();
        resizeObserver = null;
      }
      if (intersectionObserver) {
        intersectionObserver.disconnect();
        intersectionObserver = null;
      }
    };

    const setupObservers = () => {
      resizeObserver = new ResizeObserver(() => resize());
      resizeObserver.observe(canvas);

      intersectionObserver = new IntersectionObserver(onVisibilityChange, { threshold: 0.1 });
      intersectionObserver.observe(canvas);
    };

    resize();
    setupObservers();
    start();

    return { start, stop, destroy };
  }

  return {
    ParticleSystem,
    SpectrumAnalyzer,
    WaterfallRenderer,
  };
})();
