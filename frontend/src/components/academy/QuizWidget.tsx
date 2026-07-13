import { useState } from 'react'
import type { QuizData } from '../../types/academy'

interface QuizWidgetProps {
  quiz: QuizData
  onComplete: (score: number) => void
  disabled?: boolean
}

export default function QuizWidget({ quiz, onComplete, disabled }: QuizWidgetProps) {
  const [answers, setAnswers] = useState<Record<string, number>>({})
  const [submitted, setSubmitted] = useState(false)
  const [score, setScore] = useState(0)

  const handleSubmit = () => {
    let correct = 0
    quiz.questions.forEach((question) => {
      if (answers[question.id] === question.correct_index) {
        correct++
      }
    })

    const calculatedScore = Math.round((correct / quiz.questions.length) * 100)
    setScore(calculatedScore)
    setSubmitted(true)

    if (calculatedScore >= quiz.passing_score) {
      onComplete(calculatedScore)
    }
  }

  const allAnswered = quiz.questions.every((q) => answers[q.id] !== undefined)

  return (
    <div className="cyber-card space-y-4">
      <h4 className="font-bold text-cyber-blue">Quiz de comprensión</h4>

      {quiz.questions.map((question, qIndex) => (
        <div key={question.id} className="space-y-2">
          <p className="text-sm font-medium">
            {qIndex + 1}. {question.question}
          </p>
          <div className="space-y-1">
            {question.options.map((option, optionIndex) => {
              const isSelected = answers[question.id] === optionIndex
              const isCorrect = optionIndex === question.correct_index
              let className = 'block w-full text-left text-sm px-3 py-2 rounded border transition-colors '

              if (!submitted) {
                className += isSelected
                  ? 'border-cyber-blue bg-cyber-blue/10'
                  : 'border-border hover:border-cyber-blue/50'
              } else if (isCorrect) {
                className += 'border-green-500 bg-green-500/10'
              } else if (isSelected) {
                className += 'border-red-500 bg-red-500/10'
              } else {
                className += 'border-border opacity-50'
              }

              return (
                <button
                  key={option}
                  type="button"
                  className={className}
                  disabled={disabled || submitted}
                  onClick={() =>
                    setAnswers((prev) => ({ ...prev, [question.id]: optionIndex }))
                  }
                >
                  {option}
                </button>
              )
            })}
          </div>
          {submitted && (
            <p className="text-xs text-muted-foreground">{question.explanation}</p>
          )}
        </div>
      ))}

      {!submitted ? (
        <button
          type="button"
          className="cyber-button"
          disabled={disabled || !allAnswered}
          onClick={handleSubmit}
        >
          Enviar respuestas
        </button>
      ) : (
        <div className="text-sm">
          <p className="font-bold">
            Puntuación: {score}% (mínimo {quiz.passing_score}%)
          </p>
          {score >= quiz.passing_score ? (
            <p className="text-green-500 mt-1">¡Aprobado! Lección completada.</p>
          ) : (
            <p className="text-red-500 mt-1">Revisa las explicaciones e intenta de nuevo.</p>
          )}
        </div>
      )}
    </div>
  )
}
