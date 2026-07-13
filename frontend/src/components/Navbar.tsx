import { Link, useLocation, useNavigate } from 'react-router-dom'

const NAV_ITEMS = [
  { label: 'Demo', href: '#demo' },
  { label: 'Dashboard', href: '#dashboard' },
  { label: 'Academia', href: '#academy' },
  { label: 'Roadmap', href: '#roadmap' },
  { label: 'Architecture', href: '#architecture' },
]

export default function Navbar() {
  const location = useLocation()
  const navigate = useNavigate()
  const isHome = location.pathname === '/'
  const isAcademy = location.pathname.startsWith('/academy')

  const handleNavClick = (href: string) => {
    if (href.startsWith('#')) {
      if (isHome) {
        const element = document.querySelector(href)
        element?.scrollIntoView({ behavior: 'smooth' })
      } else {
        navigate(`/${href}`)
      }
    }
  }

  return (
    <header className="fixed top-0 w-full z-50 bg-[var(--glass-bg)] backdrop-blur-md border-b border-[var(--glass-border)]">
      <nav className="max-w-7xl mx-auto px-4 sm:px-8 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold text-[var(--accent-cyan)]">
          <span>⚡</span>
          <span>RF Sentinel</span>
        </Link>

        <div className="hidden md:flex items-center gap-1">
          {isHome ? (
            NAV_ITEMS.map((item) => (
              <button
                key={item.label}
                type="button"
                onClick={() => handleNavClick(item.href)}
                className={`px-4 py-2 rounded-lg text-sm transition-all ${
                  item.label === 'Demo'
                    ? 'text-[var(--accent-cyan)] bg-[rgba(0,243,255,0.15)]'
                    : 'text-[var(--text-secondary)] hover:text-[var(--accent-cyan)] hover:bg-[rgba(0,243,255,0.1)]'
                }`}
              >
                {item.label}
              </button>
            ))
          ) : (
            <>
              <Link
                to="/"
                className="px-4 py-2 rounded-lg text-sm text-[var(--text-secondary)] hover:text-[var(--accent-cyan)]"
              >
                Inicio
              </Link>
              <Link
                to="/dashboard"
                className={`px-4 py-2 rounded-lg text-sm transition-all ${
                  location.pathname === '/dashboard'
                    ? 'text-[var(--accent-cyan)] bg-[rgba(0,243,255,0.15)]'
                    : 'text-[var(--text-secondary)] hover:text-[var(--accent-cyan)]'
                }`}
              >
                Dashboard
              </Link>
              <Link
                to="/academy"
                className={`px-4 py-2 rounded-lg text-sm transition-all ${
                  isAcademy
                    ? 'text-[var(--accent-cyan)] bg-[rgba(0,243,255,0.15)]'
                    : 'text-[var(--text-secondary)] hover:text-[var(--accent-cyan)]'
                }`}
              >
                Academia
              </Link>
              <Link
                to="/targets"
                className={`px-4 py-2 rounded-lg text-sm transition-all ${
                  location.pathname === '/targets'
                    ? 'text-[var(--accent-cyan)] bg-[rgba(0,243,255,0.15)]'
                    : 'text-[var(--text-secondary)] hover:text-[var(--accent-cyan)]'
                }`}
              >
                Targets
              </Link>
              <Link
                to="/login"
                className={`px-4 py-2 rounded-lg text-sm transition-all ${
                  location.pathname === '/login'
                    ? 'text-[var(--accent-cyan)] bg-[rgba(0,243,255,0.15)]'
                    : 'text-[var(--text-secondary)] hover:text-[var(--accent-cyan)]'
                }`}
              >
                Login
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  )
}
