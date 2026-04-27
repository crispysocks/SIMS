import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { AuthState } from '@/types/auth'

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoggedIn: false,
      setAuth: (token: string, username: string, roles: string[]) => {
        set({ token, user: { username, roles }, isLoggedIn: true })
      },
      logout: () => {
        set({ user: null, token: null, isLoggedIn: false })
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
