import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import QuizWidget from './QuizWidget'

const mockQuiz = {
  questions: [
    {
      id: 'q1',
      question: '¿Qué mide la frecuencia?',
      options: ['Ciclos por segundo', 'Vatios', 'Metros'],
      correct_index: 0,
      explanation: 'La frecuencia se mide en Hz.',
    },
  ],
  passing_score: 70,
}

describe('QuizWidget', () => {
  it('completa el quiz con respuesta correcta', async () => {
    const user = userEvent.setup()
    const onComplete = vi.fn()

    render(<QuizWidget quiz={mockQuiz} onComplete={onComplete} />)

    await user.click(screen.getByRole('button', { name: /ciclos por segundo/i }))
    await user.click(screen.getByRole('button', { name: /enviar respuestas/i }))

    expect(screen.getByText(/aprobado/i)).toBeInTheDocument()
    expect(onComplete).toHaveBeenCalledWith(100)
  })

  it('muestra mensaje de reprobado con respuesta incorrecta', async () => {
    const user = userEvent.setup()
    const onComplete = vi.fn()

    render(<QuizWidget quiz={mockQuiz} onComplete={onComplete} />)

    await user.click(screen.getByRole('button', { name: /^vatios$/i }))
    await user.click(screen.getByRole('button', { name: /enviar respuestas/i }))

    expect(screen.getByText(/revisa las explicaciones/i)).toBeInTheDocument()
    expect(onComplete).not.toHaveBeenCalled()
  })

  it('permite reintentar tras reprobar', async () => {
    const user = userEvent.setup()
    const onComplete = vi.fn()

    render(<QuizWidget quiz={mockQuiz} onComplete={onComplete} />)

    await user.click(screen.getByRole('button', { name: /^vatios$/i }))
    await user.click(screen.getByRole('button', { name: /enviar respuestas/i }))
    await user.click(screen.getByRole('button', { name: /reintentar quiz/i }))

    expect(screen.getByRole('button', { name: /enviar respuestas/i })).toBeInTheDocument()
    expect(onComplete).not.toHaveBeenCalled()

    await user.click(screen.getByRole('button', { name: /ciclos por segundo/i }))
    await user.click(screen.getByRole('button', { name: /enviar respuestas/i }))

    expect(onComplete).toHaveBeenCalledWith(100)
  })
})
