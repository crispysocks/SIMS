export interface User {
  username: string
  roles: string[]
}

export interface AuthState {
  user: User | null
  token: string | null
  isLoggedIn: boolean
  setAuth: (token: string, username: string, roles: string[]) => void
  logout: () => void
  hasRole: (role: string) => boolean
}

export interface AppState {
  sidebarCollapsed: boolean
  theme: 'light' | 'dark'
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
}
