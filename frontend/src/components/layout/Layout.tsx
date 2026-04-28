import { Outlet } from 'react-router-dom'
import { useAppStore } from '@/stores/appStore'
import { Sidebar } from './Sidebar'
import { Header } from './Header'
import { cn } from '@/lib/utils'

export function Layout() {
  const { sidebarCollapsed, theme } = useAppStore()

  return (
    <div className={cn("min-h-screen bg-background", theme)}>
      <Sidebar />
      <div
        className="transition-all duration-300"
        style={{ marginLeft: sidebarCollapsed ? '64px' : '240px' }}
      >
        <div className="h-16" />
        <main className="p-6">
          <Outlet />
        </main>
      </div>
      <Header />
    </div>
  )
}
