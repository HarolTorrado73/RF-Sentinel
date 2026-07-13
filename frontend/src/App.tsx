import { useEffect, useState } from 'react'
import { Link, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Targets from './pages/Targets'
import Scans from './pages/Scans'
import Sessions from './pages/Sessions'
import AcademyHome from './pages/academy/AcademyHome'
import CourseDetail from './pages/academy/CourseDetail'
import LessonViewer from './pages/academy/LessonViewer'
import MyLearning from './pages/academy/MyLearning'
import { apiClient, endpoints } from './lib/apiClient'

interface Stats {
  users: number
  machines: number
  sessions: number
  activeSessions: number
  reports: number
  targets: number
  scans: number
}

function Dashboard() {
  const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const [stats, setStats] = useState<Stats>({
    users: 0,
    machines: 0,
    sessions: 0,
    activeSessions: 0,
    reports: 0,
    targets: 0,
    scans: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadStats = async () => {
      setLoading(true)
      try {
        const [users, targets, scans, sessions, reports] = await Promise.all([
          apiClient.get(endpoints.users.me).catch(() => null),
          apiClient.get(endpoints.targets.list).catch(() => null),
          apiClient.get(endpoints.scans.list).catch(() => null),
          apiClient.get(endpoints.sessions.list).catch(() => null),
          apiClient.get(endpoints.reports.list).catch(() => null),
        ])

        setStats({
          users: users?.data ? 1 : 0,
          machines: 0,
          sessions: sessions?.data?.length ?? 0,
          activeSessions: sessions?.data?.filter((s: { status: string }) => s.status === 'active').length ?? 0,
          reports: reports?.data?.length ?? 0,
          targets: targets?.data?.length ?? 0,
          scans: scans?.data?.length ?? 0,
        })
      } catch {
        setStats({
          users: 0,
          machines: 0,
          sessions: 0,
          activeSessions: 0,
          reports: 0,
          targets: 0,
          scans: 0,
        })
      }
      setLoading(false)
    }
    loadStats()
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold cyber-text-gradient">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Total Users', value: loading ? '-' : stats.users },
          { label: 'Total Machines', value: loading ? '-' : stats.machines },
          { label: 'Total Sessions', value: loading ? '-' : stats.sessions },
          { label: 'Active Sessions', value: loading ? '-' : stats.activeSessions, accent: true },
          { label: 'Total Targets', value: loading ? '-' : stats.targets },
          { label: 'Total Scans', value: loading ? '-' : stats.scans },
          { label: 'Total Reports', value: loading ? '-' : stats.reports },
          { label: 'System Status', value: 'Healthy', healthy: true },
        ].map((item) => (
          <div key={item.label} className="glass-card text-center">
            <h3 className="text-[var(--text-secondary)] text-sm">{item.label}</h3>
            <p
              className={`text-3xl font-bold mt-2 ${
                item.healthy ? 'text-[var(--accent-green)]' : item.accent ? 'text-[var(--accent-cyan)]' : ''
              }`}
            >
              {item.value}
            </p>
          </div>
        ))}
      </div>
      <div className="glass-card">
        <h3 className="text-lg font-bold mb-4 text-[var(--accent-cyan)]">Quick Links</h3>
        <div className="flex flex-wrap gap-4">
          <Link to="/targets" className="rf-btn rf-btn-primary">
            Manage Targets
          </Link>
          <Link to="/scans" className="rf-btn rf-btn-secondary">
            View Scans
          </Link>
          <Link to="/sessions" className="rf-btn rf-btn-secondary">
            View Sessions
          </Link>
          <a
            href={`${backendUrl}/api/v1/docs`}
            className="rf-btn rf-btn-secondary"
            target="_blank"
            rel="noopener noreferrer"
          >
            API Docs
          </a>
        </div>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <div className="min-h-screen bg-[var(--dark-bg)]">
      <Navbar />
      <main className="relative z-10 pt-16">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/login"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Login />
              </div>
            }
          />
          <Route
            path="/register"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Register />
              </div>
            }
          />
          <Route
            path="/academy"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <AcademyHome />
              </div>
            }
          />
          <Route
            path="/academy/courses/:slug"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <CourseDetail />
              </div>
            }
          />
          <Route
            path="/academy/courses/:slug/lessons/:lessonSlug"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <LessonViewer />
              </div>
            }
          />
          <Route
            path="/academy/my-learning"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <ProtectedRoute>
                  <MyLearning />
                </ProtectedRoute>
              </div>
            }
          />
          <Route
            path="/dashboard"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              </div>
            }
          />
          <Route
            path="/targets"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <ProtectedRoute>
                  <Targets />
                </ProtectedRoute>
              </div>
            }
          />
          <Route
            path="/scans"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <ProtectedRoute>
                  <Scans />
                </ProtectedRoute>
              </div>
            }
          />
          <Route
            path="/sessions"
            element={
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <ProtectedRoute>
                  <Sessions />
                </ProtectedRoute>
              </div>
            }
          />
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
    </div>
  )
}
