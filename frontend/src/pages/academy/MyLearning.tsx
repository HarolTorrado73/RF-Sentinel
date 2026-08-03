import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { apiClient, endpoints } from '../../lib/apiClient'
import { useAcademyStore } from '../../stores/academyStore'
import CourseCard from '../../components/academy/CourseCard'
import ProgressBar from '../../components/academy/ProgressBar'

export default function MyLearning() {
  const { learningSummary, setLearningSummary, setLoading, loading } = useAcademyStore()

  useEffect(() => {
    const loadLearning = async () => {
      setLoading(true)
      try {
        const res = await apiClient.get(endpoints.academy.myLearning)
        setLearningSummary(res.data)
      } catch (err) {
        console.error(err)
      }
      setLoading(false)
    }
    loadLearning()
  }, [setLearningSummary, setLoading])

  const exportProgress = () => {
    if (!learningSummary) return

    const payload = {
      exported_at: new Date().toISOString(),
      platform: 'RF Sentinel Academy',
      focus: 'educacion-investigacion-aprendizaje-responsable',
      policy: {
        excludes: ['interferencia', 'jamming', 'actividades_ilegales'],
      },
      summary: {
        enrolled_courses: learningSummary.enrolled_courses,
        completed_lessons: learningSummary.completed_lessons,
        total_lessons: learningSummary.total_lessons,
        overall_progress_percent: learningSummary.overall_progress_percent,
      },
      courses: learningSummary.courses.map((course) => ({
        slug: course.slug,
        title: course.title,
        category: course.category,
        progress_percent: course.progress_percent ?? 0,
        is_enrolled: course.is_enrolled,
        lesson_count: course.lesson_count,
      })),
    }

    const blob = new Blob([JSON.stringify(payload, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `rf-sentinel-academy-progress-${new Date().toISOString().slice(0, 10)}.json`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  if (loading || !learningSummary) {
    return <p className="text-muted-foreground">Cargando progreso...</p>
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-3xl font-bold cyber-text-gradient">Mi aprendizaje</h1>
        <button type="button" className="cyber-button" onClick={exportProgress}>
          Exportar progreso JSON
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="cyber-card text-center">
          <p className="text-muted-foreground text-sm">Cursos matriculados</p>
          <p className="text-3xl font-bold mt-2">{learningSummary.enrolled_courses}</p>
        </div>
        <div className="cyber-card text-center">
          <p className="text-muted-foreground text-sm">Lecciones completadas</p>
          <p className="text-3xl font-bold mt-2">
            {learningSummary.completed_lessons}/{learningSummary.total_lessons}
          </p>
        </div>
        <div className="cyber-card">
          <p className="text-muted-foreground text-sm mb-2">Progreso general</p>
          <ProgressBar percent={learningSummary.overall_progress_percent} />
        </div>
      </div>

      {learningSummary.courses.length === 0 ? (
        <div className="cyber-card text-center">
          <p className="text-muted-foreground mb-4">Aún no te has matriculado en ningún curso.</p>
          <Link to="/academy" className="cyber-button inline-block">
            Explorar catálogo
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {learningSummary.courses.map((course) => (
            <CourseCard key={course.slug} course={course} />
          ))}
        </div>
      )}
    </div>
  )
}
