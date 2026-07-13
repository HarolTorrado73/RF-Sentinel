import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import ProgressBar from './ProgressBar'

describe('ProgressBar', () => {
  it('muestra el porcentaje de progreso', () => {
    render(<ProgressBar percent={65} label="Progreso del curso" />)

    expect(screen.getByText('Progreso del curso')).toBeInTheDocument()
    expect(screen.getByText('65%')).toBeInTheDocument()
  })
})
