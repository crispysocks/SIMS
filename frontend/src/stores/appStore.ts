import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { AppState } from '@/types/auth'

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      theme: 'light',
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setTheme: (theme: 'light' | 'dark') => set({ theme }),
    }),
    {
      name: 'app-storage',
    }
  )
)
