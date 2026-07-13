import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import type { CourseDetail, CourseSummary, LessonDetail, UserLearningSummary } from '../types/academy'

interface AcademyState {
  courses: CourseSummary[]
  currentCourse: CourseDetail | null
  currentLesson: LessonDetail | null
  learningSummary: UserLearningSummary | null
  loading: boolean
  setCourses: (courses: CourseSummary[]) => void
  setCurrentCourse: (course: CourseDetail | null) => void
  setCurrentLesson: (lesson: LessonDetail | null) => void
  setLearningSummary: (summary: UserLearningSummary | null) => void
  setLoading: (loading: boolean) => void
}

export const useAcademyStore = create<AcademyState>()(
  devtools(
    (set) => ({
      courses: [],
      currentCourse: null,
      currentLesson: null,
      learningSummary: null,
      loading: false,
      setCourses: (courses) => set({ courses }),
      setCurrentCourse: (currentCourse) => set({ currentCourse }),
      setCurrentLesson: (currentLesson) => set({ currentLesson }),
      setLearningSummary: (learningSummary) => set({ learningSummary }),
      setLoading: (loading) => set({ loading }),
    }),
    { name: 'academy-store' }
  )
)
