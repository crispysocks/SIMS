import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { classApi } from '@/api/classes'
import { teacherApi } from '@/api/teachers'
import { useAuthStore } from '@/stores/authStore'
import { PERMISSIONS } from '@/lib/constants'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useToast } from '@/components/ui/toast'
import { Search, Plus, Trash2, Pencil } from 'lucide-react'
import { Label } from '@/components/ui/label'
import type { ClassInfo } from '@/types'

export default function ClassesPage() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const { addToast } = useToast()

  const [searchName, setSearchName] = useState('')
  const [searchNo, setSearchNo] = useState('')
  const [selectedClasses, setSelectedClasses] = useState<string[]>([])

  const [isOpen, setIsOpen] = useState(false)
  const [editing, setEditing] = useState<ClassInfo | null>(null)
  const [formData, setFormData] = useState<Partial<ClassInfo>>({})

  // 1. 分页查询班级列表（适配新 API：GET /classes?skip&limit&class_name）
  const { data: classListData, isLoading } = useQuery({
    queryKey: ['classes', 'list', 0, 100, ''],
    queryFn: () => classApi.getList(0, 100).then((r) => r.data),
  })

  // 按名称搜索（复用 getList，传入 class_name 参数）
  const { data: searchedByName } = useQuery({
    queryKey: ['classes', 'list', 0, 100, searchName],
    queryFn: () => classApi.getList(0, 100, searchName).then((r) => r.data),
    enabled: searchName.trim().length > 0,
  })

  // 按编号搜索（复用 getById）
  const { data: searchedByNo, isLoading: isNoLoading } = useQuery({
    queryKey: ['classes', 'byNo', searchNo],
    queryFn: async () => {
      try {
        const r = await classApi.getById(searchNo.trim())
        return { classes: [r.data], total: 1 }
      } catch {
        return { classes: [], total: 0 }
      }
    },
    enabled: searchNo.trim().length > 0,
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
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '添加失败', variant: 'destructive' }),
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
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '更新失败', variant: 'destructive' }),
  })

  const deleteMutation = useMutation({
    mutationFn: (classNo: string) => classApi.delete(classNo),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['classes'] })
      addToast({ title: '成功', description: '班级已删除' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '删除失败', variant: 'destructive' }),
  })

  // 决定展示的数据源
  let displayData = classListData
  if (searchNo.trim().length > 0) {
    displayData = searchedByNo
  } else if (searchName.trim().length > 0) {
    displayData = searchedByName
  }

  const displayClasses = displayData?.classes

  const toggleSelect = (classNo: string) => {
    setSelectedClasses((prev) =>
      prev.includes(classNo) ? prev.filter((n) => n !== classNo) : [...prev, classNo]
    )
  }

  const toggleSelectAll = () => {
    if (selectedClasses.length === (displayClasses?.length ?? 0)) {
      setSelectedClasses([])
    } else {
      setSelectedClasses(displayClasses?.map((c) => c.class_no) ?? [])
    }
  }

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

  const canManage = user ? PERMISSIONS.canManageStudent(user.roles) : false

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">班级管理</h2>
          <p className="text-muted-foreground">管理班级信息</p>
        </div>
        {canManage && (
          <div className="flex gap-2">
            <Button
              variant="destructive"
              size="sm"
              disabled={selectedClasses.length === 0}
              onClick={() => {
                selectedClasses.forEach((no) => deleteMutation.mutate(no))
                setSelectedClasses([])
              }}
            >
              <Trash2 className="h-4 w-4 mr-2" />
              批量删除 {selectedClasses.length > 0 && `(${selectedClasses.length})`}
            </Button>
            <Button onClick={openAdd}>
              <Plus className="h-4 w-4 mr-2" />
              新增班级
            </Button>
          </div>
        )}
      </div>

      <div className="flex gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="搜索班级编号..."
            value={searchNo}
            onChange={(e) => {
              setSearchNo(e.target.value)
              if (e.target.value.trim().length > 0) setSearchName('')
            }}
            className="pl-9"
          />
        </div>
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="搜索班级名称..."
            value={searchName}
            onChange={(e) => {
              setSearchName(e.target.value)
              if (e.target.value.trim().length > 0) setSearchNo('')
            }}
            className="pl-9"
          />
        </div>
      </div>

      <div className="border rounded-lg overflow-hidden">
        <div className="max-h-[600px] overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {canManage && (
                  <TableHead className="w-12">
                    <input
                      type="checkbox"
                      checked={displayClasses?.length === selectedClasses.length && (displayClasses?.length ?? 0) > 0}
                      onChange={toggleSelectAll}
                    />
                  </TableHead>
                )}
                <TableHead>班级编号</TableHead>
                <TableHead>班级名称</TableHead>
                <TableHead>开课时间</TableHead>
                <TableHead>班主任</TableHead>
                <TableHead>授课老师</TableHead>
                <TableHead>描述</TableHead>
                {canManage && <TableHead className="text-right">操作</TableHead>}
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading || isNoLoading ? (
                <TableRow>
                  <TableCell colSpan={canManage ? 8 : 7} className="text-center py-8">加载中...</TableCell>
                </TableRow>
              ) : displayClasses?.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={canManage ? 8 : 7} className="text-center py-8 text-muted-foreground">暂无数据</TableCell>
                </TableRow>
              ) : (
                displayClasses?.map((cls) => (
                  <TableRow key={cls.class_no}>
                    {canManage && (
                      <TableCell>
                        <input
                          type="checkbox"
                          checked={selectedClasses.includes(cls.class_no)}
                          onChange={() => toggleSelect(cls.class_no)}
                        />
                      </TableCell>
                    )}
                    <TableCell>{cls.class_no}</TableCell>
                    <TableCell className="font-medium">{cls.class_name}</TableCell>
                    <TableCell>{cls.class_open_time}</TableCell>
                    <TableCell>{cls.head_teacher_no}</TableCell>
                    <TableCell>{cls.instructor_no}</TableCell>
                    <TableCell>{cls.description || '-'}</TableCell>
                    {canManage && (
                      <TableCell className="text-right">
                        <Button variant="ghost" size="sm" onClick={() => openEdit(cls)}>
                          <Pencil className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm" onClick={() => deleteMutation.mutate(cls.class_no)}>
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
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
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editing ? '编辑班级' : '新增班级'}</DialogTitle>
          </DialogHeader>
          <div className="grid grid-cols-2 gap-4 py-4">
            <div className="space-y-2">
              <Label>班级编号</Label>
              <Input value={formData.class_no || ''} onChange={(e) => setFormData({ ...formData, class_no: e.target.value })} disabled={!!editing} />
            </div>
            <div className="space-y-2">
              <Label>班级名称</Label>
              <Input value={formData.class_name || ''} onChange={(e) => setFormData({ ...formData, class_name: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>开课时间</Label>
              <Input type="date" value={formData.class_open_time || ''} onChange={(e) => setFormData({ ...formData, class_open_time: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>班主任</Label>
              <Select value={formData.head_teacher_no || ''} onChange={(e) => setFormData({ ...formData, head_teacher_no: e.target.value })}>
                <option value="">请选择</option>
                {teachers?.map((t) => (
                  <option key={t.teacher_no} value={t.teacher_no}>{t.name}</option>
                ))}
              </Select>
            </div>
            <div className="space-y-2">
              <Label>授课老师</Label>
              <Select value={formData.instructor_no || ''} onChange={(e) => setFormData({ ...formData, instructor_no: e.target.value })}>
                <option value="">请选择</option>
                {teachers?.map((t) => (
                  <option key={t.teacher_no} value={t.teacher_no}>{t.name}</option>
                ))}
              </Select>
            </div>
            <div className="space-y-2 col-span-2">
              <Label>描述</Label>
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
