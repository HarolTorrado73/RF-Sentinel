import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import Scans from './Scans'
import { renderWithRouter, resetStores } from '../test/test-utils'
import { useScanStore } from '../stores/scanStore'

vi.mock('../lib/apiClient', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
  endpoints: {
    scans: {
      list: '/api/v1/scans',
      create: '/api/v1/scans',
    },
  },
}))

import { apiClient } from '../lib/apiClient'

describe('Scans', () => {
  beforeEach(() => {
    resetStores()
    vi.mocked(apiClient.get).mockReset()
    vi.mocked(apiClient.post).mockReset()
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] })
    useScanStore.setState({
      targets: [
        { id: 1, name: 'Server 1', value: '10.0.0.1', target_type: 'ip', status: 'active' },
      ],
    })
  })

  it('renderiza el formulario y historial vacío', async () => {
    renderWithRouter(<Scans />)

    expect(screen.getByRole('heading', { name: /scans/i })).toBeInTheDocument()
    expect(screen.getAllByRole('combobox')).toHaveLength(2)
    expect(await screen.findByText('No scans found')).toBeInTheDocument()
  })

  it('crea un scan al enviar el formulario', async () => {
    const user = userEvent.setup()
    const newScan = {
      id: 1,
      target_id: 1,
      scan_type: 'nmap',
      status: 'pending',
    }
    vi.mocked(apiClient.post).mockResolvedValueOnce({ data: newScan })

    renderWithRouter(<Scans />)

    const [targetSelect] = screen.getAllByRole('combobox')
    await user.selectOptions(targetSelect, '1')
    await user.click(screen.getByRole('button', { name: /create scan/i }))

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/api/v1/scans', {
        target_id: 1,
        scan_type: 'nmap',
      })
      expect(useScanStore.getState().scans).toHaveLength(1)
      expect(screen.getByText('Scan #1')).toBeInTheDocument()
    })
  })

  it('permite cambiar el tipo de scan', async () => {
    const user = userEvent.setup()
    renderWithRouter(<Scans />)

    const [, scanTypeSelect] = screen.getAllByRole('combobox')
    await user.selectOptions(scanTypeSelect, 'portscan')

    expect(scanTypeSelect).toHaveValue('portscan')
  })

  it('muestra estado de carga al crear scan', async () => {
    const user = userEvent.setup()
    let resolveCreate: (value: unknown) => void
    const createPromise = new Promise((resolve) => {
      resolveCreate = resolve
    })
    vi.mocked(apiClient.post).mockReturnValueOnce(createPromise as never)

    renderWithRouter(<Scans />)

    const [targetSelect] = screen.getAllByRole('combobox')
    await user.selectOptions(targetSelect, '1')
    await user.click(screen.getByRole('button', { name: /create scan/i }))

    expect(screen.getByRole('button', { name: /creating/i })).toBeDisabled()

    resolveCreate!({
      data: { id: 1, target_id: 1, scan_type: 'nmap', status: 'pending' },
    })

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /create scan/i })).toBeEnabled()
    })
  })
})
