import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import Register from './Register'
import { renderWithRouter, resetStores } from '../test/test-utils'

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
      register: '/api/v1/auth/register',
    },
  },
}))

import { apiClient } from '../lib/apiClient'

describe('Register', () => {
  beforeEach(() => {
    resetStores()
    mockNavigate.mockReset()
    vi.mocked(apiClient.post).mockReset()
  })

  it('renderiza el formulario de registro', () => {
    renderWithRouter(<Register />)

    expect(screen.getByRole('heading', { name: /register/i })).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/enter email/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/enter username/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/enter password/i)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /login/i })).toHaveAttribute('href', '/login')
  })

  it('registra usuario y redirige a login', async () => {
    const user = userEvent.setup()
    vi.mocked(apiClient.post).mockResolvedValueOnce({ data: { id: 1 } })

    renderWithRouter(<Register />)

    await user.type(screen.getByPlaceholderText(/enter email/i), 'new@test.com')
    await user.type(screen.getByPlaceholderText(/enter username/i), 'newuser')
    await user.type(screen.getByPlaceholderText(/enter password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /^register$/i }))

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/api/v1/auth/register', {
        email: 'new@test.com',
        username: 'newuser',
        password: 'password123',
      })
      expect(mockNavigate).toHaveBeenCalledWith('/login')
    })
  })

  it('muestra error cuando el registro falla', async () => {
    const user = userEvent.setup()
    vi.mocked(apiClient.post).mockRejectedValueOnce({
      response: { data: { detail: 'Email already registered' } },
    })

    renderWithRouter(<Register />)

    await user.type(screen.getByPlaceholderText(/enter email/i), 'existing@test.com')
    await user.type(screen.getByPlaceholderText(/enter username/i), 'existing')
    await user.type(screen.getByPlaceholderText(/enter password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /^register$/i }))

    expect(await screen.findByText('Email already registered')).toBeInTheDocument()
  })

  it('muestra estado de carga mientras registra', async () => {
    const user = userEvent.setup()
    let resolveRegister: (value: unknown) => void
    const registerPromise = new Promise((resolve) => {
      resolveRegister = resolve
    })
    vi.mocked(apiClient.post).mockReturnValueOnce(registerPromise as never)

    renderWithRouter(<Register />)

    await user.type(screen.getByPlaceholderText(/enter email/i), 'new@test.com')
    await user.type(screen.getByPlaceholderText(/enter username/i), 'newuser')
    await user.type(screen.getByPlaceholderText(/enter password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /^register$/i }))

    expect(screen.getByRole('button', { name: /registering/i })).toBeDisabled()

    resolveRegister!({ data: { id: 1 } })

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /^register$/i })).toBeEnabled()
    })
  })
})
