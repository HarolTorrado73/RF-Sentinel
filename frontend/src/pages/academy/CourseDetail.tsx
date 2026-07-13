import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { apiClient, endpoints } from '../../lib/apiClient'
import { useAcademyStore } from '../../stores/academyStore'
import { useAuthStore } from '../../stores/scanStore'
import ProgressBar from '../../components/academy/ProgressBar'
import ResponsibleUseBanner from '../../components/academy/ResponsibleUseBanner'
import { CATEGORY_LABELS, DIFFICULTY_LABELS } from '../../types/academy'

export default function CourseDetail() {
  const { slug } = useParams<{ slug: string }>()
  const navigate = useNavigate()
  const token = useAuthStore((state) => state.token)
  const { currentCourse, setCurrentCourse, setLoading, loading } = useAcademyStore()
  const [enrolling, setEnrolling] = useState(false)

  useEffect(() => {
    if (!slug) return

    const loadCourse = async () => {
      setLoading(true)
      try {
        const res = await apiClient.get(endpoints.academy.course(slug))
        setCurrentCourse(res.data)
      } catch (err) {
        console.error(err)
      }
      setLoading(false)
    }
    loadCourse()
  }, [slug, setCurrentCourse, setLoading])

  const handleEnroll = async () => {
    if (!token) {
      navigate('/login')
      return
    }
    if (!slug) return

    setEnrolling(true)
    try {
      await apiClient.post(endpoints.academy.enroll(slug))
      const res = await apiClient.get(endpoints.academy.course(slug))
      setCurrentCourse(res.data)
    } catch (err) {
      console.error(err)
    }
    setEnrolling(false)
  }

  if (loading || !currentCourse) {
    return <p className="text-muted-foreground">Cargando curso...</p>
  }

  return (
    <div className="space-y-6">
      <Link to="/academy" className="text-sm text-cyber-blue hover:underline">
        ← Volver al catálogo
      </Link>

      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs px-2 py-1 rounded bg-cyber-blue/20 text-cyber-blue">
          {CATEGORY_LABELS[currentCourse.category]}
        </span>
        <span className="text-xs px-2 py-1 rounded border border-border text-muted-foreground">
          {DIFFICULTY_LABELS[currentCourse.difficulty]}
        </span>
      </div>

      <h1 className="text-3xl font-bold cyber-text-gradient">{currentCourse.title}</h1>
      <p className="text-muted-foreground">{currentCourse.description}</p>

      {currentCourse.disclaimer && (
        <ResponsibleUseBanner />
      )}

      {currentCourse.is_enrolled && currentCourse.progress_percent != null && (
        <ProgressBar percent={currentCourse.progress_percent} label="Tu progreso" />
      )}

      {!currentCourse.is_enrolled && (
        <button
          type="button"
          className="cyber-button"
          disabled={enrolling}
          onClick={handleEnroll}
        >
          {enrolling ? 'Matriculando...' : token ? 'Matricularme' : 'Iniciar sesión para matricularme'}
        </button>
      )}

      <div className="cyber-card">
        <h2 className="text-xl font-bold mb-4">Lecciones</h2>
        <div className="space-y-2">
          {currentCourse.lessons.map((lesson) => (
            <Link
              key={lesson.id}
              to={`/academy/courses/${currentCourse.slug}/lessons/${lesson.slug}`}
              className="flex items-center justify-between border border-border rounded px-4 py-3 hover:border-cyber-blue/50 transition-colors"
            >
              <div>
                <p className="font-medium">{lesson.title}</p>
                <p className="text-xs text-muted-foreground">
                  {lesson.duration_minutes} min
                  {lesson.visual_type !== 'none' && ` · Visual: ${lesson.visual_type}`}
                </p>
              </div>
              <span className="text-xs text-muted-foreground">
                {lesson.status === 'completed'
                  ? '✓ Completada'
                  : lesson.status === 'in_progress'
                    ? 'En progreso'
                    : ''}
              </span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}
