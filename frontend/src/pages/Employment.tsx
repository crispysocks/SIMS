import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { employmentApi } from '@/api/employment'
import { studentApi } from '@/api/students'
import { classApi } from '@/api/classes'
import { useAuthStore } from '@/stores/authStore'
import { PERMISSIONS, EMPLOYMENT_STATUS_MAP } from '@/lib/constants'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useToast } from '@/components/ui/toast'
import { Plus, Trash2, Pencil } from 'lucide-react'
import type { Employment } from '@/types'

export default function EmploymentPage() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const { addToast } = useToast()
  const [filterType, setFilterType] = useState<'all' | 'student' | 'class' | 'salary' | 'status'>('all')
  const [filterValue, setFilterValue] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const [editing, setEditing] = useState<Employment | null>(null)
  const [formData, setFormData] = useState<Partial<Employment>>({})

  const { data: students } = useQuery({
    queryKey: ['students', 'all'],
    queryFn: () => studentApi.getAll().then((r) => r.data),
  })

  const { data: classListData } = useQuery({
    queryKey: ['classes', 'list', 0, 100, ''],
    queryFn: () => classApi.getList(0, 100).then((r) => r.data),
  })

  const classes = classListData?.classes

  const { data: employments, isLoading } = useQuery({
    queryKey: ['employment', filterType, filterValue],
    queryFn: () => {
      switch (filterType) {
        case 'student':
          return filterValue ? employmentApi.getByStudent(filterValue).then((r) => [r.data]) : Promise.resolve([])
        case 'class':
          return filterValue ? employmentApi.getByClass(filterValue).then((r) => r.data) : Promise.resolve([])
        case 'salary':
          return filterValue ? employmentApi.getBySalary(Number(filterValue)).then((r) => r.data) : Promise.resolve([])
        case 'status':
          return employmentApi.getByStatus(Number(filterValue) || 1).then((r) => r.data)
        default:
          return employmentApi.getByStatus(1).then((r) => r.data)
      }
    },
  })

  const createMutation = useMutation({
    mutationFn: ({ studentNo, data }: { studentNo: string; data: Omit<Employment, 'student_no'> }) =>
      employmentApi.create(studentNo, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employment'] })
      setIsOpen(false)
      setFormData({})
      addToast({ title: '成功', description: '就业信息已添加' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '添加失败', variant: 'destructive' }),
  })

  const updateMutation = useMutation({
    mutationFn: ({ studentNo, data }: { studentNo: string; data: Partial<Employment> }) =>
      employmentApi.update(studentNo, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employment'] })
      setIsOpen(false)
      setEditing(null)
      setFormData({})
      addToast({ title: '成功', description: '就业信息已更新' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '更新失败', variant: 'destructive' }),
  })

  const deleteMutation = useMutation({
    mutationFn: (studentNo: string) => employmentApi.delete(studentNo),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employment'] })
      addToast({ title: '成功', description: '就业信息已删除' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '删除失败', variant: 'destructive' }),
  })

  const canEdit = user ? PERMISSIONS.canEditEmployment(user.roles) : false
  const canDelete = user ? PERMISSIONS.canDeleteEmployment(user.roles) : false

  const openAdd = () => {
    setEditing(null)
    setFormData({})
    setIsOpen(true)
  }

  const openEdit = (emp: Employment) => {
    setEditing(emp)
    setFormData(emp)
    setIsOpen(true)
  }

  const handleSubmit = () => {
    if (editing) {
      updateMutation.mutate({ studentNo: editing.student_no, data: formData })
    } else if (formData.student_no) {
      const { student_no, ...rest } = formData as Employment
      createMutation.mutate({ studentNo: student_no, data: rest })
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">就业管理 v1</h2>
          <p className="text-muted-foreground">管理学生就业信息</p>
        </div>
        {canEdit && (
          <Button onClick={openAdd}>
            <Plus className="h-4 w-4 mr-2" />
            新增就业
          </Button>
        )}
      </div>

      <div className="flex gap-3 flex-wrap">
        <Select value={filterType} onChange={(e) => { setFilterType(e.target.value as typeof filterType); setFilterValue('') }} className="w-40">
          <option value="all">全部</option>
          <option value="student">按学生</option>
          <option value="class">按班级</option>
          <option value="salary">最低薪资</option>
          <option value="status">状态</option>
        </Select>

        {filterType === 'student' && (
          <Select value={filterValue} onChange={(e) => setFilterValue(e.target.value)} className="w-48">
            <option value="">选择学生</option>
            {students?.map((s) => (
              <option key={s.student_no} value={s.student_no}>{s.name}</option>
            ))}
          </Select>
        )}

        {filterType === 'class' && (
          <Select value={filterValue} onChange={(e) => setFilterValue(e.target.value)} className="w-48">
            <option value="">选择班级</option>
            {classes?.map((c) => (
              <option key={c.class_no} value={c.class_no}>{c.class_name}</option>
            ))}
          </Select>
        )}

        {filterType === 'salary' && (
          <Input type="number" placeholder="最低薪资" value={filterValue} onChange={(e) => setFilterValue(e.target.value)} className="w-48" />
        )}

        {filterType === 'status' && (
          <Select value={filterValue} onChange={(e) => setFilterValue(e.target.value)} className="w-40">
            <option value="1">正常</option>
            <option value="0">已删除</option>
          </Select>
        )}
      </div>

      <div className="border rounded-lg overflow-hidden">
        <div className="max-h-[600px] overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>学号</TableHead>
                <TableHead>公司</TableHead>
                <TableHead>岗位</TableHead>
                <TableHead>薪资</TableHead>
                <TableHead>工作地点</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>Offer时间</TableHead>
                {(canEdit || canDelete) && <TableHead className="text-right">操作</TableHead>}
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell colSpan={canEdit || canDelete ? 8 : 7} className="text-center py-8">加载中...</TableCell></TableRow>
              ) : employments?.length === 0 ? (
                <TableRow><TableCell colSpan={canEdit || canDelete ? 8 : 7} className="text-center py-8 text-muted-foreground">暂无数据</TableCell></TableRow>
              ) : (
                employments?.map((emp) => (
                  <TableRow key={emp.student_no}>
                    <TableCell>{emp.student_no}</TableCell>
                    <TableCell className="font-medium">{emp.company}</TableCell>
                    <TableCell>{emp.position}</TableCell>
                    <TableCell>{emp.salary}</TableCell>
                    <TableCell>{emp.work_location}</TableCell>
                    <TableCell>{EMPLOYMENT_STATUS_MAP[emp.employment_status]}</TableCell>
                    <TableCell>{emp.offer_time}</TableCell>
                    {(canEdit || canDelete) && (
                      <TableCell className="text-right">
                        {canEdit && (
                          <Button variant="ghost" size="sm" onClick={() => openEdit(emp)}>
                            <Pencil className="h-4 w-4" />
                          </Button>
                        )}
                        {canDelete && (
                          <Button variant="ghost" size="sm" onClick={() => deleteMutation.mutate(emp.student_no)}>
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        )}
                      </TableCell>
                    )}
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editing ? '编辑就业信息' : '新增就业信息'}</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">学生</label>
              <Select value={formData.student_no || ''} onChange={(e) => setFormData({ ...formData, student_no: e.target.value })} disabled={!!editing}>
                <option value="">请选择</option>
                {students?.map((s) => (
                  <option key={s.student_no} value={s.student_no}>{s.name} ({s.student_no})</option>
                ))}
              </Select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">公司</label>
                <Input value={formData.company || ''} onChange={(e) => setFormData({ ...formData, company: e.target.value })} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">岗位</label>
                <Input value={formData.position || ''} onChange={(e) => setFormData({ ...formData, position: e.target.value })} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">薪资</label>
                <Input type="number" value={formData.salary || ''} onChange={(e) => setFormData({ ...formData, salary: Number(e.target.value) })} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">工作地点</label>
                <Input value={formData.work_location || ''} onChange={(e) => setFormData({ ...formData, work_location: e.target.value })} />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">就业状态</label>
              <Select value={String(formData.employment_status || 1)} onChange={(e) => setFormData({ ...formData, employment_status: Number(e.target.value) })}>
                <option value="1">正常</option>
                <option value="0">已删除</option>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsOpen(false)}>取消</Button>
            <Button onClick={handleSubmit}>确认</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
