import { Link } from 'react-router-dom'
import type { CourseSummary } from '../../types/academy'
import { CATEGORY_LABELS, DIFFICULTY_LABELS } from '../../types/academy'
import ProgressBar from './ProgressBar'

interface CourseCardProps {
  course: CourseSummary
}

export default function CourseCard({ course }: CourseCardProps) {
  return (
    <div className="cyber-card flex flex-col h-full">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xs px-2 py-1 rounded bg-cyber-blue/20 text-cyber-blue">
          {CATEGORY_LABELS[course.category] ?? course.category}
        </span>
        <span className="text-xs px-2 py-1 rounded bg-cyber-card border border-border text-muted-foreground">
          {DIFFICULTY_LABELS[course.difficulty] ?? course.difficulty}
        </span>
      </div>

      <h3 className="text-lg font-bold mb-2">{course.title}</h3>
      <p className="text-muted-foreground text-sm flex-grow mb-4">{course.description}</p>

      <div className="text-xs text-muted-foreground mb-4 space-y-1">
        <p>{course.lesson_count} lecciones · {course.estimated_hours}h estimadas</p>
        {course.is_enrolled && course.progress_percent != null && (
          <ProgressBar percent={course.progress_percent} />
        )}
      </div>

      <Link to={`/academy/courses/${course.slug}`} className="cyber-button text-center">
        {course.is_enrolled ? 'Continuar' : 'Ver curso'}
      </Link>
    </div>
  )
}
