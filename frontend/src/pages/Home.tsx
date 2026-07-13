import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import HeroCanvas from '../components/HeroCanvas'
import DemoCanvas from '../components/DemoCanvas'

const ROADMAP = [
  { quarter: 'Q1 - Foundation', desc: 'API REST, SDR Core, Database', completed: true },
  { quarter: 'Q2 - ML & UI', desc: 'ML Classifier, Qt6 Dashboard', completed: false },
  { quarter: 'Q3 - Advanced', desc: 'Auto Scan, Triggers, Alerts', completed: false },
  { quarter: 'Q4 - v1.0', desc: 'Stable Release, Docker, K8s', completed: false },
]

const ARCHITECTURE = [
  { id: 'api', icon: '🔌', title: 'API', subtitle: 'Layer' },
  { id: 'sdr', icon: '📡', title: 'SDR', subtitle: 'Drivers' },
  { id: 'analysis', icon: '📊', title: 'Analysis', subtitle: 'Engine' },
  { id: 'detection', icon: '🔍', title: 'Detection', subtitle: 'Module' },
  { id: 'database', icon: '💾', title: 'Database', subtitle: 'SQLite' },
]

function AnimatedCounter({ target, suffix = '' }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0)

  useEffect(() => {
    let current = 0
    const step = Math.ceil(target / 60)
    const timer = setInterval(() => {
      current += step
      if (current >= target) {
        setCount(target)
        clearInterval(timer)
      } else {
        setCount(current)
      }
    }, 30)
    return () => clearInterval(timer)
  }, [target])

  return (
    <span>
      {count.toLocaleString()}
      {suffix}
    </span>
  )
}

export default function Home() {
  return (
    <div className="relative">
      <HeroCanvas />

      <section className="relative z-10 min-h-screen flex items-center justify-center text-center px-4">
        <div className="max-w-4xl">
          <h1 className="rf-hero-title">Radio Frequency Analysis Platform</h1>
          <p className="text-xl text-[var(--text-secondary)] mb-8 max-w-3xl mx-auto leading-relaxed">
            Plataforma Open Source profesional para análisis de radiofrecuencia en tiempo real
            usando HackRF One, RTL-SDR y tecnologías SIGINT
          </p>
          <div className="mb-8">
            <span className="rf-badge">Python 3.13+</span>
            <span className="rf-badge">FastAPI</span>
            <span className="rf-badge">PyQtGraph</span>
            <span className="rf-badge">MIT License</span>
          </div>
          <div>
            <a href="#demo" className="rf-btn rf-btn-primary">
              🔗 Ver Demo
            </a>
            <a
              href="https://github.com/HarolTorrado73/RF-Sentinel"
              className="rf-btn rf-btn-secondary"
              target="_blank"
              rel="noopener noreferrer"
            >
              ⭐ GitHub
            </a>
          </div>
        </div>
      </section>

      <section id="demo" className="relative z-10 py-24 px-4 sm:px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="rf-section-title">Live Demo</h2>
          <div className="glass-card">
            <h4 className="text-[var(--accent-cyan)] mb-4 font-semibold">Spectrum Analyzer</h4>
            <DemoCanvas type="spectrum" />
            <h4 className="text-[var(--accent-cyan)] mt-6 mb-4 font-semibold">Waterfall Monitor</h4>
            <DemoCanvas type="waterfall" />
          </div>
        </div>
      </section>

      <section id="dashboard" className="relative z-10 py-24 px-4 sm:px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="rf-section-title">Interactive Dashboard</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="glass-card text-center">
              <div className="metric-value">
                <AnimatedCounter target={6000000000} />
              </div>
              <div className="metric-label">Hz Frequency Range</div>
            </div>
            <div className="glass-card text-center">
              <div className="metric-value">
                <AnimatedCounter target={4} />
              </div>
              <div className="metric-label">SDR Devices</div>
            </div>
            <div className="glass-card text-center">
              <div className="metric-value">
                <AnimatedCounter target={128} />
              </div>
              <div className="metric-label">Signals Detected</div>
            </div>
            <div className="glass-card text-center">
              <div className="metric-value">
                <AnimatedCounter target={42} />
              </div>
              <div className="metric-label">Exports Generated</div>
            </div>
          </div>
          <div className="text-center mt-8">
            <Link to="/dashboard" className="rf-btn rf-btn-primary">
              Abrir Dashboard
            </Link>
          </div>
        </div>
      </section>

      <section id="academy" className="relative z-10 py-24 px-4 sm:px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="rf-section-title">Academia RF Sentinel</h2>
          <div className="glass-card text-center space-y-4">
            <p className="text-[var(--text-secondary)] max-w-2xl mx-auto">
              Aprende fundamentos de RF, SDR, HackRF responsable, análisis de señales e
              integración de hardware con cursos interactivos y visualizaciones simuladas.
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              <span className="rf-badge">RF Fundamentos</span>
              <span className="rf-badge">SDR</span>
              <span className="rf-badge">HackRF</span>
              <span className="rf-badge">Señales</span>
              <span className="rf-badge">Hardware</span>
            </div>
            <Link to="/academy" className="rf-btn rf-btn-primary">
              Explorar Academia
            </Link>
          </div>
        </div>
      </section>

      <section id="roadmap" className="relative z-10 py-24 px-4 sm:px-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="rf-section-title">Roadmap Interactive</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {ROADMAP.map((item) => (
              <div
                key={item.quarter}
                className={`glass-card ${item.completed ? 'border-l-4 border-l-[var(--accent-green)]' : ''}`}
              >
                <h4 className="text-[var(--accent-cyan)] font-bold mb-2">{item.quarter}</h4>
                <p className="text-[var(--text-secondary)] text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="architecture" className="relative z-10 py-24 px-4 sm:px-8 pb-32">
        <div className="max-w-6xl mx-auto">
          <h2 className="rf-section-title">Interactive Architecture</h2>
          <div className="flex flex-wrap justify-center gap-6">
            {ARCHITECTURE.map((node) => (
              <div
                key={node.id}
                className="glass-card min-w-[150px] text-center cursor-default hover:scale-105 transition-transform"
              >
                <div className="text-2xl mb-2">{node.icon}</div>
                <div className="font-bold">{node.title}</div>
                <div className="text-sm text-[var(--text-secondary)]">{node.subtitle}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="relative z-10 border-t border-[var(--glass-border)] bg-[var(--glass-bg)] backdrop-blur-md py-12 text-center">
        <p className="text-[var(--text-secondary)]">© 2026 RF Sentinel Project. MIT License.</p>
        <div className="flex justify-center gap-8 mt-4">
          <a
            href="https://github.com/HarolTorrado73/RF-Sentinel"
            className="text-[var(--text-secondary)] hover:text-[var(--accent-cyan)] transition-colors"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
          <Link to="/login" className="text-[var(--text-secondary)] hover:text-[var(--accent-cyan)]">
            Login
          </Link>
        </div>
      </footer>
    </div>
  )
}
