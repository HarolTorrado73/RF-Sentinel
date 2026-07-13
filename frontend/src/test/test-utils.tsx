import { render, type RenderOptions } from '@testing-library/react'
import { MemoryRouter, type MemoryRouterProps } from 'react-router-dom'
import type { ReactElement, ReactNode } from 'react'
import { useAuthStore, useScanStore } from '../stores/scanStore'
import { useAcademyStore } from '../stores/academyStore'

interface RouterOptions extends Omit<MemoryRouterProps, 'children'> {
  route?: string
}

interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  router?: RouterOptions
}

export function resetStores() {
  useAuthStore.setState({ token: null, user: null })
  useScanStore.setState({
    targets: [],
    scans: [],
    reports: [],
    loading: false,
  })
  useAcademyStore.setState({
    courses: [],
    currentCourse: null,
    currentLesson: null,
    learningSummary: null,
    loading: false,
  })
}

function createWrapper(router?: RouterOptions) {
  const { route = '/', ...routerProps } = router ?? {}

  return function Wrapper({ children }: { children: ReactNode }) {
    return (
      <MemoryRouter initialEntries={[route]} {...routerProps}>
        {children}
      </MemoryRouter>
    )
  }
}

export function renderWithRouter(ui: ReactElement, options?: CustomRenderOptions) {
  const { router, ...renderOptions } = options ?? {}
  return render(ui, { wrapper: createWrapper(router), ...renderOptions })
}
