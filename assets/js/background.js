const ParticleSystem = (canvasId) => {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext("2d");
  let particles = [];
  const particleCount = 100;
  const connectionDistance = 120;

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };

  const init = () => {
    particles = [];
    for (let i = 0; i < particleCount; i++) {
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
    ctx.fillStyle = "rgba(10, 15, 26, 0.1)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width) p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(0, 243, 255, 0.6)";
      ctx.fill();
    }

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < connectionDistance) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(0, 243, 255, ${0.15 * (1 - dist / connectionDistance)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  };

  let rafId = null;
  const start = () => {
    const loop = () => {
      update();
      rafId = requestAnimationFrame(loop);
    };
    loop();
  };

  const stop = () => {
    if (rafId) cancelAnimationFrame(rafId);
  };

  window.addEventListener('resize', resize);
  resize();
  init();

  return { start, stop };
};

const RFBackgroundAnimation = (canvasId) => {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext("2d");
  let waves = [];
  const maxWaves = 8;

  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };

  const init = () => {
    waves = [];
    for (let i = 0; i < maxWaves; i++) {
      waves.push({
        radius: 0,
        maxRadius: Math.max(canvas.width, canvas.height) * 0.6,
        speed: 0.3 + i * 0.1,
        opacity: 0,
      });
    }
  };

  const update = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;

    for (const w of waves) {
      w.radius += w.speed;
      if (w.radius > w.maxRadius) {
        w.radius = 0;
        w.opacity = 0.25;
      }
      const progress = w.radius / w.maxRadius;
      const alpha = 0.25 * (1 - progress);
      ctx.beginPath();
      ctx.arc(cx, cy, w.radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(0, 243, 255, ${alpha})`;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
  };

  let rafId = null;
  const start = () => {
    const loop = () => {
      update();
      rafId = requestAnimationFrame(loop);
    };
    loop();
  };

  const stop = () => {
    if (rafId) cancelAnimationFrame(rafId);
  };

  window.addEventListener('resize', resize);
  resize();
  init();

  return { start, stop };
};

window.Background = {
  ParticleSystem,
  RFBackgroundAnimation
};