import { useState } from 'react'
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
import { Search, Plus, Trash2, RotateCcw } from 'lucide-react'
import { Label } from '@/components/ui/label'
import type { Student } from '@/types'

export default function StudentsPage() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const { addToast } = useToast()
  const [searchName, setSearchName] = useState('')
  const [searchNo, setSearchNo] = useState('')
  const [selectedClass, setSelectedClass] = useState('')
  const [selectedStudents, setSelectedStudents] = useState<string[]>([])
  const [isAddOpen, setIsAddOpen] = useState(false)
  const [formData, setFormData] = useState<Partial<Student>>({})

  const { data: students, isLoading } = useQuery({
    queryKey: ['students', 'all'],
    queryFn: () => studentApi.getAll().then((r) => r.data),
  })

  const { data: searchedByName } = useQuery({
    queryKey: ['students', 'search', searchName],
    queryFn: () => studentApi.search(searchName).then((r) => r.data),
    enabled: searchName.trim().length > 0,
  })

  const { data: searchedByNo, isLoading: isNoLoading } = useQuery({
    queryKey: ['students', 'byNo', searchNo],
    queryFn: async () => {
      try {
        const r = await studentApi.getById(searchNo.trim())
        return [r.data]
      } catch {
        return []
      }
    },
    enabled: searchNo.trim().length > 0,
  })

  const { data: studentsByClass, isLoading: isClassLoading } = useQuery({
    queryKey: ['students', 'class', selectedClass],
    queryFn: () => studentApi.getByClass(selectedClass).then((r) => r.data),
    enabled: selectedClass.length > 0,
  })

  const { data: classListData } = useQuery({
    queryKey: ['classes', 'list', 0, 100, ''],
    queryFn: () => classApi.getList(0, 100).then((r) => r.data),
  })

  const classes = classListData?.classes

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

  let displayStudents = students
  if (selectedClass.length > 0) {
    displayStudents = studentsByClass
  } else if (searchNo.trim().length > 0) {
    displayStudents = searchedByNo
  } else if (searchName.trim().length > 0) {
    displayStudents = searchedByName
  }

  const toggleSelect = (studentNo: string) => {
    setSelectedStudents((prev) =>
      prev.includes(studentNo) ? prev.filter((n) => n !== studentNo) : [...prev, studentNo]
    )
  }

  const toggleSelectAll = () => {
    if (selectedStudents.length === (displayStudents?.length ?? 0)) {
      setSelectedStudents([])
    } else {
      setSelectedStudents(displayStudents?.map((s) => s.student_no) ?? [])
    }
  }

  const handleRestore = () => {
    const no = searchNo.trim()
    if (!no) {
      addToast({ title: '提示', description: '请输入要恢复的学号', variant: 'destructive' })
      return
    }
    restoreMutation.mutate([no])
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
          <div className="flex gap-2">
            <Button
              variant="destructive"
              size="sm"
              disabled={selectedStudents.length === 0}
              onClick={() => deleteMutation.mutate(selectedStudents)}
            >
              <Trash2 className="h-4 w-4 mr-2" />
              批量删除 {selectedStudents.length > 0 && `(${selectedStudents.length})`}
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={searchNo.trim().length === 0}
              onClick={handleRestore}
            >
              <RotateCcw className="h-4 w-4 mr-2" />
              恢复学生
            </Button>
            <Button onClick={() => setIsAddOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              新增学生
            </Button>
          </div>
        )}
      </div>

      <div className="flex gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="搜索学号..."
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
            placeholder="搜索姓名..."
            value={searchName}
            onChange={(e) => {
              setSearchName(e.target.value)
              if (e.target.value.trim().length > 0) setSearchNo('')
            }}
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

      <div className="border rounded-lg overflow-hidden">
        <div className="max-h-[600px] overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {canManage && (
                  <TableHead className="w-12">
                    <input
                      type="checkbox"
                      checked={displayStudents?.length === selectedStudents.length && displayStudents?.length > 0}
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
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading || isNoLoading || isClassLoading ? (
                <TableRow>
                  <TableCell colSpan={canManage ? 7 : 6} className="text-center py-8">加载中...</TableCell>
                </TableRow>
              ) : displayStudents?.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={canManage ? 7 : 6} className="text-center py-8 text-muted-foreground">暂无数据</TableCell>
                </TableRow>
              ) : (
                displayStudents?.map((student) => (
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
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>

      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>新增学生</DialogTitle>
          </DialogHeader>
          <div className="grid grid-cols-2 gap-4 py-4">
            <div className="space-y-2">
              <Label>学号</Label>
              <Input value={formData.student_no || ''} onChange={(e) => setFormData({ ...formData, student_no: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>姓名</Label>
              <Input value={formData.name || ''} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>性别</Label>
              <Select value={formData.gender || ''} onChange={(e) => setFormData({ ...formData, gender: e.target.value })}>
                <option value="">请选择</option>
                <option value="男">男</option>
                <option value="女">女</option>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>年龄</Label>
              <Input type="number" value={formData.age || ''} onChange={(e) => setFormData({ ...formData, age: Number(e.target.value) })} />
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
            <div className="space-y-2">
              <Label>籍贯</Label>
              <Input value={formData.birth_place || ''} onChange={(e) => setFormData({ ...formData, birth_place: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>毕业院校</Label>
              <Input value={formData.graduate_school || ''} onChange={(e) => setFormData({ ...formData, graduate_school: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>专业</Label>
              <Input value={formData.major || ''} onChange={(e) => setFormData({ ...formData, major: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>入学时间</Label>
              <Input type="date" value={formData.entrance_time || ''} onChange={(e) => setFormData({ ...formData, entrance_time: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>毕业时间</Label>
              <Input type="date" value={formData.graduate_time || ''} onChange={(e) => setFormData({ ...formData, graduate_time: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>学历</Label>
              <Input value={formData.education || ''} onChange={(e) => setFormData({ ...formData, education: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>导师姓名</Label>
              <Input value={formData.advisor_name || ''} onChange={(e) => setFormData({ ...formData, advisor_name: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>身份证号</Label>
              <Input value={formData.id_card || ''} onChange={(e) => setFormData({ ...formData, id_card: e.target.value })} />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAddOpen(false)}>取消</Button>
            <Button onClick={() => createMutation.mutate(formData as Student)}>确定</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
