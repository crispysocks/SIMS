import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { teacherApi } from '@/api/teachers'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useToast } from '@/components/ui/toast'
import { Plus, Trash2, Pencil, Search, PieChart } from 'lucide-react'
import type { Teacher } from '@/types'
import { useNavigate } from 'react-router-dom'

export default function TeachersPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { addToast } = useToast()
  const [isOpen, setIsOpen] = useState(false)
  const [editing, setEditing] = useState<Teacher | null>(null)
  const [formData, setFormData] = useState<Partial<Teacher>>({})
  const [selectedTeachers, setSelectedTeachers] = useState<string[]>([])

  const { data: teachers, isLoading } = useQuery({
    queryKey: ['teachers', 'all'],
    queryFn: () => teacherApi.getAll().then((r) => r.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: Teacher) => teacherApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['teachers'] })
      setIsOpen(false)
      setFormData({})
      addToast({ title: '成功', description: '教师已添加' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '添加失败', variant: 'destructive' }),
  })

  const updateMutation = useMutation({
    mutationFn: ({ teacherNo, data }: { teacherNo: string; data: Partial<Teacher> }) => teacherApi.update(teacherNo, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['teachers'] })
      setIsOpen(false)
      setEditing(null)
      setFormData({})
      addToast({ title: '成功', description: '教师已更新' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '更新失败', variant: 'destructive' }),
  })

  const deleteMutation = useMutation({
    mutationFn: (teacherNos: string[]) => teacherApi.delete(teacherNos),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['teachers'] })
      setSelectedTeachers([])
      addToast({ title: '成功', description: '教师已删除' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '删除失败', variant: 'destructive' }),
  })

  const openAdd = () => {
    setEditing(null)
    setFormData({})
    setIsOpen(true)
  }

  const openEdit = (teacher: Teacher) => {
    setEditing(teacher)
    setFormData(teacher)
    setIsOpen(true)
  }

  const handleSubmit = () => {
    if (editing) {
      updateMutation.mutate({ teacherNo: editing.teacher_no, data: formData })
    } else {
      createMutation.mutate(formData as Teacher)
    }
  }

  const toggleSelect = (teacherNo: string) => {
    setSelectedTeachers((prev) =>
      prev.includes(teacherNo) ? prev.filter((n) => n !== teacherNo) : [...prev, teacherNo]
    )
  }

  const toggleSelectAll = () => {
    if (selectedTeachers.length === (teachers?.length ?? 0)) {
      setSelectedTeachers([])
    } else {
      setSelectedTeachers(teachers?.map((t) => t.teacher_no) ?? [])
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">教师管理</h2>
          <p className="text-muted-foreground">管理教师信息</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => navigate('/teachers/search')}>
            <Search className="h-4 w-4 mr-2" />
            查询教师
          </Button>
          <Button variant="outline" onClick={() => navigate('/teachers/stats')}>
            <PieChart className="h-4 w-4 mr-2" />
            性别统计
          </Button>
          <Button
            variant="destructive"
            size="sm"
            disabled={selectedTeachers.length === 0}
            onClick={() => deleteMutation.mutate(selectedTeachers)}
          >
            <Trash2 className="h-4 w-4 mr-2" />
            批量删除 {selectedTeachers.length > 0 && `(${selectedTeachers.length})`}
          </Button>
          <Button onClick={openAdd}>
            <Plus className="h-4 w-4 mr-2" />
            新增教师
          </Button>
        </div>
      </div>

      <div className="border rounded-lg overflow-hidden">
        <div className="max-h-[600px] overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12">
                  <input
                    type="checkbox"
                    checked={teachers?.length === selectedTeachers.length && (teachers?.length ?? 0) > 0}
                    onChange={toggleSelectAll}
                  />
                </TableHead>
                <TableHead>教师编号</TableHead>
                <TableHead>姓名</TableHead>
                <TableHead>性别</TableHead>
                <TableHead>电话</TableHead>
                <TableHead>邮箱</TableHead>
                <TableHead>授课科目</TableHead>
                <TableHead className="text-right">操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell colSpan={8} className="text-center py-8">加载中...</TableCell></TableRow>
              ) : teachers?.length === 0 ? (
                <TableRow><TableCell colSpan={8} className="text-center py-8 text-muted-foreground">暂无数据</TableCell></TableRow>
              ) : (
                teachers?.map((teacher) => (
                  <TableRow key={teacher.teacher_no}>
                    <TableCell>
                      <input
                        type="checkbox"
                        checked={selectedTeachers.includes(teacher.teacher_no)}
                        onChange={() => toggleSelect(teacher.teacher_no)}
                      />
                    </TableCell>
                    <TableCell>{teacher.teacher_no}</TableCell>
                    <TableCell className="font-medium">{teacher.name}</TableCell>
                    <TableCell>{teacher.gender}</TableCell>
                    <TableCell>{teacher.phone}</TableCell>
                    <TableCell>{teacher.email}</TableCell>
                    <TableCell>{teacher.subject}</TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" onClick={() => openEdit(teacher)}>
                        <Pencil className="h-4 w-4" />
                      </Button>
                    </TableCell>
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
            <DialogTitle>{editing ? '编辑教师' : '新增教师'}</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">教师编号</label>
                <Input value={formData.teacher_no || ''} onChange={(e) => setFormData({ ...formData, teacher_no: e.target.value })} disabled={!!editing} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">姓名</label>
                <Input value={formData.name || ''} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">性别</label>
                <select className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm" value={formData.gender || ''} onChange={(e) => setFormData({ ...formData, gender: e.target.value })}>
                  <option value="">请选择</option>
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">电话</label>
                <Input value={formData.phone || ''} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">邮箱</label>
              <Input value={formData.email || ''} onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">授课科目</label>
              <Input value={formData.subject || ''} onChange={(e) => setFormData({ ...formData, subject: e.target.value })} />
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
