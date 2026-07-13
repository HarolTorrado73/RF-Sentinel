import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import Targets from './Targets'
import { renderWithRouter, resetStores } from '../test/test-utils'
import { useScanStore } from '../stores/scanStore'

vi.mock('../lib/apiClient', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
  endpoints: {
    targets: {
      list: '/api/v1/targets',
      create: '/api/v1/targets',
    },
  },
}))

import { apiClient } from '../lib/apiClient'

describe('Targets', () => {
  beforeEach(() => {
    resetStores()
    vi.mocked(apiClient.get).mockReset()
    vi.mocked(apiClient.post).mockReset()
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] })
  })

  it('renderiza el formulario y lista vacía', async () => {
    renderWithRouter(<Targets />)

    expect(screen.getByRole('heading', { name: /targets/i })).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/target name/i)).toBeInTheDocument()
    expect(screen.getByPlaceholderText(/ip, domain, or cidr/i)).toBeInTheDocument()
    expect(screen.getByRole('combobox')).toBeInTheDocument()
    expect(await screen.findByText('No targets configured')).toBeInTheDocument()
  })

  it('envía el formulario y agrega un target', async () => {
    const user = userEvent.setup()
    const newTarget = {
      id: 1,
      name: 'Server 1',
      value: '192.168.1.1',
      target_type: 'ip' as const,
      status: 'active',
    }
    vi.mocked(apiClient.post).mockResolvedValueOnce({ data: newTarget })

    renderWithRouter(<Targets />)

    await user.type(screen.getByPlaceholderText(/target name/i), 'Server 1')
    await user.type(screen.getByPlaceholderText(/ip, domain, or cidr/i), '192.168.1.1')
    await user.click(screen.getByRole('button', { name: /add target/i }))

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/api/v1/targets', {
        name: 'Server 1',
        value: '192.168.1.1',
        target_type: 'ip',
      })
      expect(useScanStore.getState().targets).toHaveLength(1)
      expect(screen.getByText('Server 1')).toBeInTheDocument()
    })
  })

  it('permite seleccionar tipo de target', async () => {
    const user = userEvent.setup()
    renderWithRouter(<Targets />)

    const typeSelect = screen.getByRole('combobox')
    await user.selectOptions(typeSelect, 'domain')

    expect(typeSelect).toHaveValue('domain')
  })

  it('muestra estado de carga al agregar target', async () => {
    const user = userEvent.setup()
    let resolveCreate: (value: unknown) => void
    const createPromise = new Promise((resolve) => {
      resolveCreate = resolve
    })
    vi.mocked(apiClient.post).mockReturnValueOnce(createPromise as never)

    renderWithRouter(<Targets />)

    await user.type(screen.getByPlaceholderText(/target name/i), 'Server 1')
    await user.type(screen.getByPlaceholderText(/ip, domain, or cidr/i), '192.168.1.1')
    await user.click(screen.getByRole('button', { name: /add target/i }))

    expect(screen.getByRole('button', { name: /adding/i })).toBeDisabled()

    resolveCreate!({
      data: {
        id: 1,
        name: 'Server 1',
        value: '192.168.1.1',
        target_type: 'ip',
        status: 'active',
      },
    })

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /add target/i })).toBeEnabled()
    })
  })
})
