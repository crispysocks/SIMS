import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Users,
  GraduationCap,
  School,
  FileText,
  Briefcase,
  BarChart3,
} from 'lucide-react'
import { studentApi } from '@/api/students'
import { teacherApi } from '@/api/teachers'
import { classApi } from '@/api/classes'
import { employmentApi } from '@/api/employment'

const stats = [
  { label: '学生总数', icon: Users, color: 'text-blue-500', bg: 'bg-blue-500/10', api: studentApi.getAll },
  { label: '教师总数', icon: GraduationCap, color: 'text-green-500', bg: 'bg-green-500/10', api: teacherApi.getAll },
  { label: '班级总数', icon: School, color: 'text-purple-500', bg: 'bg-purple-500/10', api: classApi.getTotalCount },
  { label: '就业人数', icon: Briefcase, color: 'text-orange-500', bg: 'bg-orange-500/10', api: () => employmentApi.getByStatus(1) },
]

const quickLinks = [
  { label: '学生管理', icon: Users, path: '/students', desc: '查看和管理学生信息' },
  { label: '成绩管理', icon: FileText, path: '/scores', desc: '录入和查询成绩' },
  { label: '就业管理', icon: Briefcase, path: '/employment', desc: '跟踪学生就业情况' },
  { label: '统计分析', icon: BarChart3, path: '/statistics', desc: '查看数据报表' },
]

export default function DashboardPage() {
  const navigate = useNavigate()

  const { data: students } = useQuery({ queryKey: ['students', 'all'], queryFn: () => studentApi.getAll().then((r) => r.data) })
  const { data: teachers } = useQuery({ queryKey: ['teachers', 'all'], queryFn: () => teacherApi.getAll().then((r) => r.data) })
  const { data: classCountRes } = useQuery({ queryKey: ['classes', 'count'], queryFn: () => classApi.getTotalCount().then((r) => r.data) })
  const { data: employments } = useQuery({ queryKey: ['employment', 'status', 1], queryFn: () => employmentApi.getByStatus(1).then((r) => r.data) })

  const counts = [students?.length, teachers?.length, classCountRes?.total, employments?.length]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">仪表盘</h2>
        <p className="text-muted-foreground">系统概览与快捷入口</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={stat.label}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">{stat.label}</CardTitle>
                <div className={`${stat.bg} p-2 rounded-md`}>
                  <Icon className={`h-4 w-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{counts[index] ?? '-'}</div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">快捷入口</h3>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {quickLinks.map((link) => {
            const Icon = link.icon
            return (
              <Card
                key={link.path}
                className="cursor-pointer hover:bg-accent/50 transition-colors"
                onClick={() => navigate(link.path)}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-center gap-3">
                    <div className="bg-primary/10 p-2 rounded-md">
                      <Icon className="h-5 w-5 text-primary" />
                    </div>
                    <CardTitle className="text-base">{link.label}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription>{link.desc}</CardDescription>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>
    </div>
  )
}
