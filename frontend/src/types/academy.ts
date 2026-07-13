export interface LessonSummary {
  id: number
  slug: string
  title: string
  order_index: number
  duration_minutes: number
  visual_type: string
  status?: string | null
}

export interface CourseSummary {
  id: number
  slug: string
  title: string
  description: string
  category: string
  difficulty: string
  estimated_hours: number
  lesson_count: number
  progress_percent?: number | null
  is_enrolled: boolean
}

export interface CourseDetail extends Omit<CourseSummary, 'lesson_count'> {
  disclaimer?: string | null
  lessons: LessonSummary[]
}

export interface LessonDetail {
  id: number
  slug: string
  title: string
  content_type: string
  content: string
  visual_type: string
  visual_data?: Record<string, unknown> | null
  quiz?: QuizData | null
  duration_minutes: number
  course_slug: string
  course_title: string
  status?: string | null
  quiz_score?: number | null
}

export interface QuizQuestion {
  id: string
  question: string
  options: string[]
  correct_index: number
  explanation: string
}

export interface QuizData {
  questions: QuizQuestion[]
  passing_score: number
}

export interface UserLearningSummary {
  enrolled_courses: number
  completed_lessons: number
  total_lessons: number
  overall_progress_percent: number
  courses: CourseSummary[]
}

export const CATEGORY_LABELS: Record<string, string> = {
  rf: 'RF',
  sdr: 'SDR',
  hackrf: 'HackRF',
  signals: 'Señales',
  hardware: 'Hardware',
}

export const DIFFICULTY_LABELS: Record<string, string> = {
  beginner: 'Principiante',
  intermediate: 'Intermedio',
  advanced: 'Avanzado',
}
