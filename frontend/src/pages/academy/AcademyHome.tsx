import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { apiClient, endpoints } from '../../lib/apiClient'
import { useAcademyStore } from '../../stores/academyStore'
import CourseCard from '../../components/academy/CourseCard'
import ResponsibleUseBanner from '../../components/academy/ResponsibleUseBanner'
import { useAuthStore } from '../../stores/scanStore'

export default function AcademyHome() {
  const { courses, loading, setCourses, setLoading } = useAcademyStore()
  const token = useAuthStore((state) => state.token)

  useEffect(() => {
    const loadCourses = async () => {
      setLoading(true)
      try {
        const res = await apiClient.get(endpoints.academy.courses)
        setCourses(res.data)
      } catch (err) {
        console.error(err)
      }
      setLoading(false)
    }
    loadCourses()
  }, [setCourses, setLoading])

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-extrabold cyber-text-gradient">Academia RF Sentinel</h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Plataforma educativa sobre SDR y radiofrecuencia. Aprende fundamentos, análisis de
          señales e integración de hardware con enfoque en investigación responsable.
        </p>
        {token && (
          <Link to="/academy/my-learning" className="cyber-button inline-block">
            Mi aprendizaje
          </Link>
        )}
      </div>

      <ResponsibleUseBanner />

      {loading ? (
        <p className="text-center text-muted-foreground">Cargando cursos...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <CourseCard key={course.slug} course={course} />
          ))}
        </div>
      )}

      <div className="cyber-card text-center">
        <h3 className="font-bold mb-2">Enfoque educativo</h3>
        <p className="text-sm text-muted-foreground">
          Educación · Investigación · Aprendizaje responsable. Sin interferencia ni actividades
          ilegales.
        </p>
      </div>
    </div>
  )
}
