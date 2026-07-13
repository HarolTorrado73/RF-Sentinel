import { screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { Route, Routes } from 'react-router-dom'
import App from './App'
import ProtectedRoute from './components/ProtectedRoute'
import { renderWithRouter, resetStores } from './test/test-utils'
import { useAuthStore } from './stores/scanStore'

vi.mock('./lib/apiClient', () => ({
  apiClient: {
    get: vi.fn().mockResolvedValue({ data: [] }),
    post: vi.fn(),
  },
  endpoints: {
    auth: { login: '/api/v1/auth/login', register: '/api/v1/auth/register' },
    users: { me: '/api/v1/users/me' },
    targets: { list: '/api/v1/targets', create: '/api/v1/targets' },
    scans: { list: '/api/v1/scans', create: '/api/v1/scans' },
    sessions: { list: '/api/v1/sessions' },
    reports: { list: '/api/v1/reports' },
  },
}))

describe('Navegación', () => {
  beforeEach(() => {
    resetStores()
  })

  it('muestra la página de inicio en la ruta raíz', () => {
    renderWithRouter(<App />, { router: { route: '/' } })

    expect(
      screen.getByRole('heading', { name: /radio frequency analysis platform/i })
    ).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /abrir dashboard/i })).toHaveAttribute(
      'href',
      '/dashboard'
    )
    expect(screen.getByRole('link', { name: /explorar academia/i })).toHaveAttribute(
      'href',
      '/academy'
    )
  })

  it('redirige rutas protegidas a login sin autenticación', () => {
    renderWithRouter(<App />, { router: { route: '/dashboard' } })

    expect(screen.getByRole('heading', { name: /^login$/i })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: /^dashboard$/i })).not.toBeInTheDocument()
  })

  it('permite acceder al dashboard con token válido', async () => {
    useAuthStore.setState({ token: 'valid-token', user: { username: 'test', role: 'viewer' } })

    renderWithRouter(<App />, { router: { route: '/dashboard' } })

    expect(await screen.findByRole('heading', { name: /^dashboard$/i })).toBeInTheDocument()
  })

  it('muestra login en la ruta /login', () => {
    renderWithRouter(<App />, { router: { route: '/login' } })

    expect(screen.getByRole('heading', { name: /^login$/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /register/i })).toHaveAttribute('href', '/register')
  })
})

describe('Rutas con ProtectedRoute', () => {
  beforeEach(() => {
    resetStores()
  })

  it('redirige a login cuando no hay token', () => {
    renderWithRouter(
      <Routes>
        <Route path="/login" element={<div>Página de login</div>} />
        <Route
          path="/targets"
          element={
            <ProtectedRoute>
              <div>Targets protegidos</div>
            </ProtectedRoute>
          }
        />
      </Routes>,
      { router: { route: '/targets' } }
    )

    expect(screen.getByText('Página de login')).toBeInTheDocument()
    expect(screen.queryByText('Targets protegidos')).not.toBeInTheDocument()
  })
})
