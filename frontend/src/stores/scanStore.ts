import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import type { Target, Scan, Report } from '../types'

interface ScanState {
  targets: Target[]
  scans: Scan[]
  reports: Report[]
  loading: boolean
  setTargets: (targets: Target[]) => void
  addTarget: (target: Target) => void
  setScans: (scans: Scan[]) => void
  addScan: (scan: Scan) => void
  setReports: (reports: Report[]) => void
  setLoading: (loading: boolean) => void
}

export const useScanStore = create<ScanState>()(
  devtools(
    (set) => ({
      targets: [],
      scans: [],
      reports: [],
      loading: false,
      setTargets: (targets) => set({ targets }),
      addTarget: (target) =>
        set((state) => ({ targets: [...state.targets, target] })),
      setScans: (scans) => set({ scans }),
      addScan: (scan) => set((state) => ({ scans: [scan, ...state.scans] })),
      setReports: (reports) => set({ reports }),
      setLoading: (loading) => set({ loading }),
    }),
    { name: 'scan-store' }
  )
)

interface AuthState {
  token: string | null
  user: { username: string; role: string } | null
  setToken: (token: string | null) => void
  setUser: (user: { username: string; role: string } | null) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  devtools(
    (set) => ({
      token: null,
      user: null,
      setToken: (token) => set({ token }),
      setUser: (user) => set({ user }),
      logout: () => set({ token: null, user: null }),
    }),
    { name: 'auth-store' }
  )
)