import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { AuthState } from '@/types/auth'

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isLoggedIn: false,
      login: (username: string, roles: string[]) => {
        set({ user: { username, roles }, isLoggedIn: true })
      },
      logout: () => {
        set({ user: null, isLoggedIn: false })
      },
      hasRole: (role: string) => {
        const { user } = get()
        return user?.roles.includes(role) ?? false
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
