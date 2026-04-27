import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { scoreApi } from '@/api/scores'
import { studentApi } from '@/api/students'
import { useAuthStore } from '@/stores/authStore'
import { PERMISSIONS } from '@/lib/constants'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/components/ui/toast'
import { Plus, Trash2, Pencil, Search } from 'lucide-react'
import type { Score } from '@/types'

export default function ScoresPage() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const { addToast } = useToast()
  const [searchStudentNo, setSearchStudentNo] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const [editing, setEditing] = useState<Score | null>(null)
  const [formData, setFormData] = useState<Partial<Score>>({})

  const { data: students } = useQuery({
    queryKey: ['students', 'all'],
    queryFn: () => studentApi.getAll().then((r) => r.data),
  })

  const { data: scores, isLoading } = useQuery({
    queryKey: ['scores', searchStudentNo],
    queryFn: () => {
      if (searchStudentNo) {
        return scoreApi.getByStudent(searchStudentNo).then((r) => r.data)
      }
      return Promise.resolve([] as Score[])
    },
    enabled: !!searchStudentNo,
  })

  const createMutation = useMutation({
    mutationFn: (data: Score) => scoreApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scores'] })
      setIsOpen(false)
      setFormData({})
      addToast({ title: '成功', description: '成绩已录入' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '录入失败', variant: 'destructive' }),
  })

  const updateMutation = useMutation({
    mutationFn: (data: Score) => scoreApi.update(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scores'] })
      setIsOpen(false)
      setEditing(null)
      setFormData({})
      addToast({ title: '成功', description: '成绩已更新' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '更新失败', variant: 'destructive' }),
  })

  const deleteMutation = useMutation({
    mutationFn: (data: { student_no: string; exam_no: string; exam_name: string }) => scoreApi.delete(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scores'] })
      addToast({ title: '成功', description: '成绩已删除' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '删除失败', variant: 'destructive' }),
  })

  const canEdit = user ? PERMISSIONS.canEditScore(user.roles) : false
  const canDelete = user ? PERMISSIONS.canDeleteScore(user.roles) : false

  const openAdd = () => {
    setEditing(null)
    setFormData({})
    setIsOpen(true)
  }

  const openEdit = (score: Score) => {
    setEditing(score)
    setFormData(score)
    setIsOpen(true)
  }

  const handleSubmit = () => {
    if (editing) {
      updateMutation.mutate(formData as Score)
    } else {
      createMutation.mutate(formData as Score)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">成绩管理</h2>
          <p className="text-muted-foreground">查询和管理学生成绩</p>
        </div>
        {canEdit && (
          <Button onClick={openAdd}>
            <Plus className="h-4 w-4 mr-2" />
            录入成绩
          </Button>
        )}
      </div>

      <div className="flex gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="输入学号查询成绩..."
            value={searchStudentNo}
            onChange={(e) => setSearchStudentNo(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      <div className="border rounded-lg overflow-hidden">
        <div className="max-h-[600px] overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>学号</TableHead>
                <TableHead>考试编号</TableHead>
                <TableHead>考试名称</TableHead>
                <TableHead>成绩</TableHead>
                <TableHead>考试日期</TableHead>
                {(canEdit || canDelete) && <TableHead className="text-right">操作</TableHead>}
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell colSpan={canEdit || canDelete ? 6 : 5} className="text-center py-8">加载中...</TableCell></TableRow>
              ) : !searchStudentNo ? (
                <TableRow><TableCell colSpan={canEdit || canDelete ? 6 : 5} className="text-center py-8 text-muted-foreground">请输入学号查询成绩</TableCell></TableRow>
              ) : scores?.length === 0 ? (
                <TableRow><TableCell colSpan={canEdit || canDelete ? 6 : 5} className="text-center py-8 text-muted-foreground">暂无成绩记录</TableCell></TableRow>
              ) : (
                scores?.map((score) => (
                  <TableRow key={`${score.student_no}-${score.exam_no}-${score.exam_name}`}>
                    <TableCell>{score.student_no}</TableCell>
                    <TableCell>{score.exam_no}</TableCell>
                    <TableCell>{score.exam_name}</TableCell>
                    <TableCell>
                      <Badge variant={score.score >= 60 ? 'default' : 'destructive'}>
                        {score.score}
                      </Badge>
                    </TableCell>
                    <TableCell>{score.exam_date}</TableCell>
                    {(canEdit || canDelete) && (
                      <TableCell className="text-right">
                        {canEdit && (
                          <Button variant="ghost" size="sm" onClick={() => openEdit(score)}>
                            <Pencil className="h-4 w-4" />
                          </Button>
                        )}
                        {canDelete && (
                          <Button variant="ghost" size="sm" onClick={() => deleteMutation.mutate(score)}>
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
            <DialogTitle>{editing ? '编辑成绩' : '录入成绩'}</DialogTitle>
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
                <label className="text-sm font-medium">考试编号</label>
                <Input value={formData.exam_no || ''} onChange={(e) => setFormData({ ...formData, exam_no: e.target.value })} disabled={!!editing} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">考试名称</label>
                <Input value={formData.exam_name || ''} onChange={(e) => setFormData({ ...formData, exam_name: e.target.value })} disabled={!!editing} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">成绩</label>
                <Input type="number" value={formData.score || ''} onChange={(e) => setFormData({ ...formData, score: Number(e.target.value) })} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">考试日期</label>
                <Input type="date" value={formData.exam_date || ''} onChange={(e) => setFormData({ ...formData, exam_date: e.target.value })} />
              </div>
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
