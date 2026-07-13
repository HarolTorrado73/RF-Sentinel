import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { apiClient, endpoints } from '../../lib/apiClient'
import { useAcademyStore } from '../../stores/academyStore'
import { useAuthStore } from '../../stores/scanStore'
import DiagramVisualizer from '../../components/academy/DiagramVisualizer'
import LessonContent from '../../components/academy/LessonContent'
import QuizWidget from '../../components/academy/QuizWidget'
import SpectrumVisualizer from '../../components/academy/SpectrumVisualizer'
import WaveformVisualizer from '../../components/academy/WaveformVisualizer'

export default function LessonViewer() {
  const { slug, lessonSlug } = useParams<{ slug: string; lessonSlug: string }>()
  const navigate = useNavigate()
  const token = useAuthStore((state) => state.token)
  const { currentLesson, setCurrentLesson, setLoading, loading } = useAcademyStore()
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!slug || !lessonSlug) return

    const loadLesson = async () => {
      setLoading(true)
      try {
        const res = await apiClient.get(endpoints.academy.lesson(slug, lessonSlug))
        setCurrentLesson(res.data)

        if (token && res.data.status !== 'completed') {
          await apiClient.put(endpoints.academy.lessonProgress(res.data.id), {
            status: 'in_progress',
          })
        }
      } catch (err) {
        console.error(err)
      }
      setLoading(false)
    }
    loadLesson()
  }, [slug, lessonSlug, setCurrentLesson, setLoading, token])

  const handleQuizComplete = async (score: number) => {
    if (!currentLesson || !token) return

    setSaving(true)
    try {
      const res = await apiClient.put(endpoints.academy.lessonProgress(currentLesson.id), {
        status: 'completed',
        quiz_score: score,
      })
      setCurrentLesson(res.data)
    } catch (err) {
      console.error(err)
    }
    setSaving(false)
  }

  const handleMarkComplete = async () => {
    if (!currentLesson || !token) {
      navigate('/login')
      return
    }

    setSaving(true)
    try {
      const res = await apiClient.put(endpoints.academy.lessonProgress(currentLesson.id), {
        status: 'completed',
      })
      setCurrentLesson(res.data)
    } catch (err) {
      console.error(err)
    }
    setSaving(false)
  }

  if (loading || !currentLesson) {
    return <p className="text-muted-foreground">Cargando lección...</p>
  }

  const visualData = currentLesson.visual_data ?? {}

  return (
    <div className="space-y-6">
      <Link
        to={`/academy/courses/${currentLesson.course_slug}`}
        className="text-sm text-cyber-blue hover:underline"
      >
        ← {currentLesson.course_title}
      </Link>

      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold cyber-text-gradient">{currentLesson.title}</h1>
        {currentLesson.status === 'completed' && (
          <span className="text-sm text-green-500 font-medium">Completada</span>
        )}
      </div>

      <div className="cyber-card">
        <LessonContent content={currentLesson.content} />
      </div>

      {currentLesson.visual_type === 'spectrum' && (
        <SpectrumVisualizer data={visualData as never} />
      )}
      {currentLesson.visual_type === 'waveform' && (
        <WaveformVisualizer data={visualData as never} />
      )}
      {currentLesson.visual_type === 'diagram' && (
        <DiagramVisualizer data={visualData as never} />
      )}

      {currentLesson.quiz ? (
        <QuizWidget
          quiz={currentLesson.quiz}
          onComplete={handleQuizComplete}
          disabled={saving || currentLesson.status === 'completed'}
        />
      ) : (
        token && currentLesson.status !== 'completed' && (
          <button
            type="button"
            className="cyber-button"
            disabled={saving}
            onClick={handleMarkComplete}
          >
            {saving ? 'Guardando...' : 'Marcar como completada'}
          </button>
        )
      )}

      {!token && (
        <p className="text-sm text-muted-foreground">
          <Link to="/login" className="text-cyber-blue hover:underline">
            Inicia sesión
          </Link>{' '}
          para guardar tu progreso.
        </p>
      )}
    </div>
  )
}
