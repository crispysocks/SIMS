export interface User {
  username: string
  roles: string[]
}

export interface AuthState {
  user: User | null
  isLoggedIn: boolean
  login: (username: string, roles: string[]) => void
  logout: () => void
  hasRole: (role: string) => boolean
}

export interface AppState {
  sidebarCollapsed: boolean
  theme: 'light' | 'dark'
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
}
