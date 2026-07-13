import { screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import Navbar from './Navbar'
import { renderWithRouter } from '../test/test-utils'

describe('Navbar', () => {
  it('muestra navegación de landing en la página de inicio', () => {
    renderWithRouter(<Navbar />, { router: { route: '/' } })

    expect(screen.getByRole('link', { name: /rf sentinel/i })).toHaveAttribute('href', '/')
    expect(screen.getByRole('button', { name: /demo/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /academia/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /roadmap/i })).toBeInTheDocument()
  })

  it('muestra navegación de aplicación en rutas internas', () => {
    renderWithRouter(<Navbar />, { router: { route: '/targets' } })

    expect(screen.getByRole('link', { name: /inicio/i })).toHaveAttribute('href', '/')
    expect(screen.getByRole('link', { name: /dashboard/i })).toHaveAttribute('href', '/dashboard')
    expect(screen.getByRole('link', { name: /academia/i })).toHaveAttribute('href', '/academy')
    expect(screen.getByRole('link', { name: /targets/i })).toHaveAttribute('href', '/targets')
    expect(screen.getByRole('link', { name: /login/i })).toHaveAttribute('href', '/login')
  })

  it('resalta el enlace activo según la ruta actual', () => {
    renderWithRouter(<Navbar />, { router: { route: '/targets' } })

    const targetsLink = screen.getByRole('link', { name: /targets/i })
    const dashboardLink = screen.getByRole('link', { name: /dashboard/i })

    expect(targetsLink.className).toContain('accent-cyan')
    expect(dashboardLink.className).not.toContain('bg-[rgba(0,243,255,0.15)]')
  })
})
