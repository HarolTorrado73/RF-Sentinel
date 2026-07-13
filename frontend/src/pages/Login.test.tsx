import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import Login from './Login'
import { renderWithRouter, resetStores } from '../test/test-utils'
import { useAuthStore } from '../stores/scanStore'

const mockNavigate = vi.fn()

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

vi.mock('../lib/apiClient', () => ({
  apiClient: {
    post: vi.fn(),
  },
  endpoints: {
    auth: {
      login: '/api/v1/auth/login',
    },
  },
}))

import { apiClient } from '../lib/apiClient'

describe('Login', () => {
  beforeEach(() => {
    resetStores()
    mockNavigate.mockReset()
    vi.mocked(apiClient.post).mockReset()
  })

  it('renderiza el formulario de inicio de sesión', () => {
    renderWithRouter(<Login />)

    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/enter email/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/enter password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /register/i })).toHaveAttribute('href', '/register')
  })

  it('muestra error cuando las credenciales son inválidas', async () => {
    const user = userEvent.setup()
    vi.mocked(apiClient.post).mockRejectedValueOnce({
      response: { data: { detail: 'Invalid credentials' } },
    })

    renderWithRouter(<Login />)

    await user.type(screen.getByPlaceholderText(/enter email/i), 'user@test.com')
    await user.type(screen.getByPlaceholderText(/enter password/i), 'wrong-password')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    expect(await screen.findByText('Invalid credentials')).toBeInTheDocument()
    expect(mockNavigate).not.toHaveBeenCalled()
  })

  it('inicia sesión correctamente y navega al dashboard', async () => {
    const user = userEvent.setup()
    vi.mocked(apiClient.post).mockResolvedValueOnce({
      data: { access_token: 'test-token', token_type: 'bearer' },
    })

    renderWithRouter(<Login />)

    await user.type(screen.getByPlaceholderText(/enter email/i), 'user@test.com')
    await user.type(screen.getByPlaceholderText(/enter password/i), 'secret123')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    await waitFor(() => {
      expect(useAuthStore.getState().token).toBe('test-token')
      expect(useAuthStore.getState().user).toEqual({
        username: 'user@test.com',
        role: 'viewer',
      })
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard')
    })
  })

  it('muestra estado de carga mientras inicia sesión', async () => {
    const user = userEvent.setup()
    let resolveLogin: (value: unknown) => void
    const loginPromise = new Promise((resolve) => {
      resolveLogin = resolve
    })
    vi.mocked(apiClient.post).mockReturnValueOnce(loginPromise as never)

    renderWithRouter(<Login />)

    await user.type(screen.getByPlaceholderText(/enter email/i), 'user@test.com')
    await user.type(screen.getByPlaceholderText(/enter password/i), 'secret123')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    const submitButton = screen.getByRole('button', { name: /signing in/i })
    expect(submitButton).toBeDisabled()

    resolveLogin!({ data: { access_token: 'test-token' } })

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /sign in/i })).toBeEnabled()
    })
  })
})
