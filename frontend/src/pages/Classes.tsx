import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { classApi } from '@/api/classes'
import { teacherApi } from '@/api/teachers'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useToast } from '@/components/ui/toast'
import { Plus, Trash2, Pencil, Users } from 'lucide-react'
import type { ClassInfo } from '@/types'

export default function ClassesPage() {
  const queryClient = useQueryClient()
  const { addToast } = useToast()
  const [isOpen, setIsOpen] = useState(false)
  const [editing, setEditing] = useState<ClassInfo | null>(null)
  const [formData, setFormData] = useState<Partial<ClassInfo>>({})

  const { data: classes, isLoading } = useQuery({
    queryKey: ['classes', 'all'],
    queryFn: () => classApi.getAll().then((r) => r.data),
  })

  const { data: teachers } = useQuery({
    queryKey: ['teachers', 'all'],
    queryFn: () => teacherApi.getAll().then((r) => r.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: ClassInfo) => classApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['classes'] })
      setIsOpen(false)
      setFormData({})
      addToast({ title: '成功', description: '班级已添加' })
    },
    onError: () => addToast({ title: '错误', description: '添加失败', variant: 'destructive' }),
  })

  const updateMutation = useMutation({
    mutationFn: ({ classNo, data }: { classNo: string; data: Partial<ClassInfo> }) => classApi.update(classNo, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['classes'] })
      setIsOpen(false)
      setEditing(null)
      setFormData({})
      addToast({ title: '成功', description: '班级已更新' })
    },
    onError: () => addToast({ title: '错误', description: '更新失败', variant: 'destructive' }),
  })

  const deleteMutation = useMutation({
    mutationFn: (classNo: string) => classApi.delete(classNo),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['classes'] })
      addToast({ title: '成功', description: '班级已删除' })
    },
    onError: () => addToast({ title: '错误', description: '删除失败', variant: 'destructive' }),
  })

  const openAdd = () => {
    setEditing(null)
    setFormData({})
    setIsOpen(true)
  }

  const openEdit = (cls: ClassInfo) => {
    setEditing(cls)
    setFormData(cls)
    setIsOpen(true)
  }

  const handleSubmit = () => {
    if (editing) {
      updateMutation.mutate({ classNo: editing.class_no, data: formData })
    } else {
      createMutation.mutate(formData as ClassInfo)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">班级管理</h2>
          <p className="text-muted-foreground">管理班级信息</p>
        </div>
        <Button onClick={openAdd}>
          <Plus className="h-4 w-4 mr-2" />
          新增班级
        </Button>
      </div>

      <div className="border rounded-lg overflow-hidden">
        <div className="max-h-[600px] overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>班级编号</TableHead>
                <TableHead>班级名称</TableHead>
                <TableHead>开课时间</TableHead>
                <TableHead>班主任</TableHead>
                <TableHead>授课老师</TableHead>
                <TableHead className="text-right">操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell colSpan={6} className="text-center py-8">加载中...</TableCell></TableRow>
              ) : classes?.length === 0 ? (
                <TableRow><TableCell colSpan={6} className="text-center py-8 text-muted-foreground">暂无数据</TableCell></TableRow>
              ) : (
                classes?.map((cls) => (
                  <TableRow key={cls.class_no}>
                    <TableCell>{cls.class_no}</TableCell>
                    <TableCell className="font-medium">{cls.class_name}</TableCell>
                    <TableCell>{cls.class_open_time}</TableCell>
                    <TableCell>{cls.head_teacher_no}</TableCell>
                    <TableCell>{cls.instructor_no}</TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" onClick={() => openEdit(cls)}>
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm" onClick={() => deleteMutation.mutate(cls.class_no)}>
                        <Trash2 className="h-4 w-4 text-destructive" />
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
            <DialogTitle>{editing ? '编辑班级' : '新增班级'}</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">班级编号</label>
                <Input value={formData.class_no || ''} onChange={(e) => setFormData({ ...formData, class_no: e.target.value })} disabled={!!editing} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">班级名称</label>
                <Input value={formData.class_name || ''} onChange={(e) => setFormData({ ...formData, class_name: e.target.value })} />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">开课时间</label>
              <Input type="date" value={formData.class_open_time || ''} onChange={(e) => setFormData({ ...formData, class_open_time: e.target.value })} />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">班主任</label>
              <select className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm" value={formData.head_teacher_no || ''} onChange={(e) => setFormData({ ...formData, head_teacher_no: e.target.value })}>
                <option value="">请选择</option>
                {teachers?.map((t) => (
                  <option key={t.teacher_no} value={t.teacher_no}>{t.name}</option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">授课老师</label>
              <select className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm" value={formData.instructor_no || ''} onChange={(e) => setFormData({ ...formData, instructor_no: e.target.value })}>
                <option value="">请选择</option>
                {teachers?.map((t) => (
                  <option key={t.teacher_no} value={t.teacher_no}>{t.name}</option>
                ))}
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">描述</label>
              <Input value={formData.description || ''} onChange={(e) => setFormData({ ...formData, description: e.target.value })} />
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
