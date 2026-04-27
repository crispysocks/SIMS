import { useNavigate, useLocation } from 'react-router-dom'
import { useAppStore } from '@/stores/appStore'
import { useAuthStore } from '@/stores/authStore'
import {
  LayoutDashboard,
  Users,
  GraduationCap,
  School,
  FileText,
  Briefcase,
  BriefcaseBusiness,
  BarChart3,
  Shield,
  Menu,
  ChevronLeft,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const menuItems = [
  { icon: LayoutDashboard, label: '仪表盘', path: '/' },
  { icon: Users, label: '学生管理', path: '/students' },
  { icon: GraduationCap, label: '教师管理', path: '/teachers' },
  { icon: School, label: '班级管理', path: '/classes' },
  { icon: FileText, label: '成绩管理', path: '/scores' },
  { icon: Briefcase, label: '就业管理 v1', path: '/employment' },
  { icon: BriefcaseBusiness, label: '就业管理 v2', path: '/employment-v2' },
  { icon: BarChart3, label: '统计分析', path: '/statistics' },
  { icon: Shield, label: '用户管理', path: '/users', adminOnly: true },
]

export function Sidebar() {
  const navigate = useNavigate()
  const location = useLocation()
  const { sidebarCollapsed, toggleSidebar } = useAppStore()
  const { user } = useAuthStore()

  return (
    <aside
      className={cn(
        "fixed left-0 top-0 z-40 h-screen bg-card border-r border-border transition-all duration-300 flex flex-col",
        sidebarCollapsed ? "w-16" : "w-60"
      )}
    >
      <div className="flex h-16 items-center justify-between px-4 border-b border-border">
        {!sidebarCollapsed && (
          <span className="text-lg font-bold text-primary truncate">SIMS</span>
        )}
        <button
          onClick={toggleSidebar}
          className="p-1.5 rounded-md hover:bg-accent text-muted-foreground hover:text-foreground transition-colors"
        >
          {sidebarCollapsed ? <Menu className="h-5 w-5" /> : <ChevronLeft className="h-5 w-5" />}
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-1">
        {menuItems.map((item) => {
          if (item.adminOnly && !user?.roles.includes('admin')) {
            return null
          }
          const isActive = location.pathname === item.path || location.pathname.startsWith(`${item.path}/`)
          const Icon = item.icon
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={cn(
                "flex items-center w-full rounded-md px-3 py-2.5 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground",
                sidebarCollapsed && "justify-center px-2"
              )}
              title={sidebarCollapsed ? item.label : undefined}
            >
              <Icon className={cn("h-5 w-5 flex-shrink-0", !sidebarCollapsed && "mr-3")} />
              {!sidebarCollapsed && <span className="truncate">{item.label}</span>}
            </button>
          )
        })}
      </nav>

      {!sidebarCollapsed && user && (
        <div className="p-4 border-t border-border">
          <div className="text-xs text-muted-foreground">当前用户</div>
          <div className="text-sm font-medium truncate">{user.username}</div>
          <div className="text-xs text-muted-foreground mt-1">
            {user.roles.join(', ')}
          </div>
        </div>
      )}
    </aside>
  )
}
