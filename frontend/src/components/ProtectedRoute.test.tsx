import { screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { Route, Routes } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'
import { renderWithRouter, resetStores } from '../test/test-utils'
import { useAuthStore } from '../stores/scanStore'

describe('ProtectedRoute', () => {
  it('redirige a login cuando no hay token', () => {
    resetStores()
    renderWithRouter(
      <Routes>
        <Route path="/login" element={<div>Página de login</div>} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <div>Contenido protegido</div>
            </ProtectedRoute>
          }
        />
      </Routes>,
      { router: { route: '/dashboard' } }
    )

    expect(screen.getByText('Página de login')).toBeInTheDocument()
    expect(screen.queryByText('Contenido protegido')).not.toBeInTheDocument()
  })

  it('renderiza el contenido cuando hay token', () => {
    resetStores()
    useAuthStore.setState({ token: 'valid-token', user: { username: 'test', role: 'viewer' } })

    renderWithRouter(
      <ProtectedRoute>
        <div>Contenido protegido</div>
      </ProtectedRoute>
    )

    expect(screen.getByText('Contenido protegido')).toBeInTheDocument()
  })
})
