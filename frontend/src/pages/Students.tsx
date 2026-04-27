import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { studentApi } from '@/api/students'
import { classApi } from '@/api/classes'
import { useAuthStore } from '@/stores/authStore'
import { PERMISSIONS, GENDER_MAP } from '@/lib/constants'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useToast } from '@/components/ui/toast'
import { Search, Plus, Trash2, RotateCcw, Eye } from 'lucide-react'
import { Label } from '@/components/ui/label'
import type { Student } from '@/types'

export default function StudentsPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const { addToast } = useToast()
  const [searchName, setSearchName] = useState('')
  const [selectedClass, setSelectedClass] = useState('')
  const [selectedStudents, setSelectedStudents] = useState<string[]>([])
  const [isAddOpen, setIsAddOpen] = useState(false)
  const [formData, setFormData] = useState<Partial<Student>>({})

  const { data: students, isLoading } = useQuery({
    queryKey: ['students', 'all'],
    queryFn: () => studentApi.getAll().then((r) => r.data),
  })

  const { data: classes } = useQuery({
    queryKey: ['classes', 'all'],
    queryFn: () => classApi.getAll().then((r) => r.data),
  })

  const deleteMutation = useMutation({
    mutationFn: (noList: string[]) => studentApi.batchDelete(noList),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] })
      setSelectedStudents([])
      addToast({ title: '成功', description: '学生已删除' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '删除失败', variant: 'destructive' }),
  })

  const restoreMutation = useMutation({
    mutationFn: (noList: string[]) => studentApi.batchRestore(noList),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] })
      setSelectedStudents([])
      addToast({ title: '成功', description: '学生已恢复' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '恢复失败', variant: 'destructive' }),
  })

  const createMutation = useMutation({
    mutationFn: (data: Student) => studentApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] })
      setIsAddOpen(false)
      setFormData({})
      addToast({ title: '成功', description: '学生已添加' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '添加失败', variant: 'destructive' }),
  })

  const filteredStudents = students?.filter((s) => {
    const matchName = !searchName || s.name.includes(searchName)
    const matchClass = !selectedClass || s.class_no === selectedClass
    return matchName && matchClass
  })

  const toggleSelect = (studentNo: string) => {
    setSelectedStudents((prev) =>
      prev.includes(studentNo) ? prev.filter((n) => n !== studentNo) : [...prev, studentNo]
    )
  }

  const toggleSelectAll = () => {
    if (selectedStudents.length === (filteredStudents?.length ?? 0)) {
      setSelectedStudents([])
    } else {
      setSelectedStudents(filteredStudents?.map((s) => s.student_no) ?? [])
    }
  }

  const canManage = user ? PERMISSIONS.canManageStudent(user.roles) : false

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">学生管理</h2>
          <p className="text-muted-foreground">管理学生信息</p>
        </div>
        {canManage && (
          <Button onClick={() => setIsAddOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            新增学生
          </Button>
        )}
      </div>

      <div className="flex gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="搜索姓名..."
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select value={selectedClass} onChange={(e) => setSelectedClass(e.target.value)} className="w-48">
          <option value="">全部班级</option>
          {classes?.map((c) => (
            <option key={c.class_no} value={c.class_no}>{c.class_name}</option>
          ))}
        </Select>
      </div>

      {canManage && selectedStudents.length > 0 && (
        <div className="flex gap-2">
          <Button variant="destructive" size="sm" onClick={() => deleteMutation.mutate(selectedStudents)}>
            <Trash2 className="h-4 w-4 mr-2" />
            批量删除 ({selectedStudents.length})
          </Button>
          <Button variant="outline" size="sm" onClick={() => restoreMutation.mutate(selectedStudents)}>
            <RotateCcw className="h-4 w-4 mr-2" />
            批量恢复
          </Button>
        </div>
      )}

      <div className="border rounded-lg overflow-hidden">
        <div className="max-h-[600px] overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {canManage && (
                  <TableHead className="w-12">
                    <input
                      type="checkbox"
                      checked={filteredStudents?.length === selectedStudents.length && filteredStudents?.length > 0}
                      onChange={toggleSelectAll}
                    />
                  </TableHead>
                )}
                <TableHead>学号</TableHead>
                <TableHead>姓名</TableHead>
                <TableHead>性别</TableHead>
                <TableHead>班级</TableHead>
                <TableHead>电话</TableHead>
                <TableHead>年龄</TableHead>
                <TableHead className="text-right">操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={canManage ? 8 : 7} className="text-center py-8">加载中...</TableCell>
                </TableRow>
              ) : filteredStudents?.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={canManage ? 8 : 7} className="text-center py-8 text-muted-foreground">暂无数据</TableCell>
                </TableRow>
              ) : (
                filteredStudents?.map((student) => (
                  <TableRow key={student.student_no}>
                    {canManage && (
                      <TableCell>
                        <input
                          type="checkbox"
                          checked={selectedStudents.includes(student.student_no)}
                          onChange={() => toggleSelect(student.student_no)}
                        />
                      </TableCell>
                    )}
                    <TableCell>{student.student_no}</TableCell>
                    <TableCell className="font-medium">{student.name}</TableCell>
                    <TableCell>{GENDER_MAP[student.gender] || student.gender}</TableCell>
                    <TableCell>{student.class_no}</TableCell>
                    <TableCell>{student.phone ?? '-'}</TableCell>
                    <TableCell>{student.age ?? '-'}</TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" onClick={() => navigate(`/students/${student.student_no}`)}>
                        <Eye className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>

      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>新增学生</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>学号</Label>
                <Input value={formData.student_no || ''} onChange={(e) => setFormData({ ...formData, student_no: e.target.value })} />
              </div>
              <div className="space-y-2">
                <Label>姓名</Label>
                <Input value={formData.name || ''} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>性别</Label>
                <Select value={formData.gender || ''} onChange={(e) => { const val = e.target.value; setFormData(prev => ({ ...prev, gender: val })) }}>
                  <option value="">请选择</option>
                  <option value="男">男</option>
                  <option value="女">女</option>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>年龄</Label>
                <Input type="number" value={formData.age ?? ''} onChange={(e) => setFormData({ ...formData, age: e.target.value ? Number(e.target.value) : undefined })} />
              </div>
            </div>
            <div className="space-y-2">
              <Label>班级</Label>
              <Select value={formData.class_no || ''} onChange={(e) => setFormData({ ...formData, class_no: e.target.value })}>
                <option value="">请选择</option>
                {classes?.map((c) => (
                  <option key={c.class_no} value={c.class_no}>{c.class_name}</option>
                ))}
              </Select>
            </div>
            <div className="space-y-2">
              <Label>电话</Label>
              <Input value={formData.phone || ''} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>入学时间</Label>
                <Input type="date" value={formData.entrance_time || ''} onChange={(e) => setFormData({ ...formData, entrance_time: e.target.value })} />
              </div>
              <div className="space-y-2">
                <Label>学历</Label>
                <Select value={formData.education || ''} onChange={(e) => setFormData({ ...formData, education: e.target.value })}>
                  <option value="">请选择</option>
                  <option value="专科">专科</option>
                  <option value="本科">本科</option>
                  <option value="硕士">硕士</option>
                </Select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>身份证号</Label>
                <Input value={formData.id_card || ''} onChange={(e) => setFormData({ ...formData, id_card: e.target.value })} />
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAddOpen(false)}>取消</Button>
            <Button onClick={() => createMutation.mutate(formData as Student)}>确认</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
