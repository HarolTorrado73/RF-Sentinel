import { screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import AcademyHome from './AcademyHome'
import { renderWithRouter, resetStores } from '../../test/test-utils'

vi.mock('../../lib/apiClient', () => ({
  apiClient: {
    get: vi.fn(),
  },
  endpoints: {
    academy: {
      courses: '/api/v1/academy/courses',
    },
  },
}))

import { apiClient } from '../../lib/apiClient'

const mockCourses = [
  {
    id: 1,
    slug: 'rf-fundamentos',
    title: 'Fundamentos de Radiofrecuencia',
    description: 'Aprende RF',
    category: 'rf',
    difficulty: 'beginner',
    estimated_hours: 2,
    lesson_count: 3,
    is_enrolled: false,
  },
]

describe('AcademyHome', () => {
  beforeEach(() => {
    resetStores()
    vi.mocked(apiClient.get).mockReset()
    vi.mocked(apiClient.get).mockResolvedValue({ data: mockCourses })
  })

  it('renderiza el catálogo de cursos', async () => {
    renderWithRouter(<AcademyHome />)

    expect(screen.getByRole('heading', { name: /academia rf sentinel/i })).toBeInTheDocument()
    expect(screen.getByText(/uso responsable/i)).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText('Fundamentos de Radiofrecuencia')).toBeInTheDocument()
    })
  })
})
