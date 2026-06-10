function showModule(name) {
  window.Modals.open(name);
}

function initCounters() {
  const counters = [
    { id: 'range-counter', value: 6e9, suffix: 'Hz', decimals: 1 },
    { id: 'devices-counter', value: 5 },
    { id: 'signals-counter', value: 1247 },
    { id: 'exports-counter', value: 89 }
  ];

  counters.forEach(c => {
    let current = 0;
    const increment = c.value / 50;
    const el = document.getElementById(c.id);
    const timer = setInterval(() => {
      current += increment;
      if (current >= c.value) {
        current = c.value;
        clearInterval(timer);
      }
      el.textContent = c.decimals ? current.toFixed(1) : Math.floor(current).toLocaleString();
      if (c.suffix) el.textContent += ' ' + c.suffix;
    }, 30);
  });
}

function navTo(el) {
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
  el.classList.add('active');
}

document.addEventListener('DOMContentLoaded', () => {
  const bgParticles = window.Background.ParticleSystem('hero-canvas');
  if (bgParticles) bgParticles.start();

  const spectrum = window.Spectrum.SpectrumAnalyzer('spectrum-canvas');
  const waterfall = window.Waterfall.Waterfall('waterfall-canvas');
  if (spectrum) spectrum.start();
  if (waterfall) waterfall.start();

  window.Dashboard.initDashboard();
  window.Modals.init();
  initCounters();

  document.querySelectorAll('.nav-links a').forEach(a => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (href && href.startsWith('#')) {
        e.preventDefault();
        document.querySelector(href)?.scrollIntoView({ behavior: 'smooth' });
        navTo(a);
      }
    });
  });
});