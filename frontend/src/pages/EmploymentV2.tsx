import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { employmentV2Api, type EmploymentQuery } from '@/api/employmentV2'
import { studentApi } from '@/api/students'
import { useAuthStore } from '@/stores/authStore'
import { PERMISSIONS, EMPLOYMENT_STATUS_MAP } from '@/lib/constants'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { useToast } from '@/components/ui/toast'
import { Plus, Trash2, Pencil, RotateCcw } from 'lucide-react'
import type { EmploymentV2 } from '@/types'

export default function EmploymentV2Page() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const { addToast } = useToast()
  const [query, setQuery] = useState<EmploymentQuery>({})
  const [selectedItems, setSelectedItems] = useState<string[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const [editing, setEditing] = useState<EmploymentV2 | null>(null)
  const [formData, setFormData] = useState<Partial<EmploymentV2>>({})

  const { data: students } = useQuery({
    queryKey: ['students', 'all'],
    queryFn: () => studentApi.getAll().then((r) => r.data),
  })

  const { data: employments, isLoading } = useQuery({
    queryKey: ['employmentV2', query],
    queryFn: () => employmentV2Api.search(query).then((r) => r.data),
  })

  const createMutation = useMutation({
    mutationFn: (data: EmploymentV2) => employmentV2Api.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employmentV2'] })
      setIsOpen(false)
      setFormData({})
      addToast({ title: '成功', description: '就业信息已添加' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '添加失败', variant: 'destructive' }),
  })

  const updateMutation = useMutation({
    mutationFn: ({ studentNo, data }: { studentNo: string; data: Partial<EmploymentV2> }) =>
      employmentV2Api.update(studentNo, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employmentV2'] })
      setIsOpen(false)
      setEditing(null)
      setFormData({})
      addToast({ title: '成功', description: '就业信息已更新' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '更新失败', variant: 'destructive' }),
  })

  const deleteMutation = useMutation({
    mutationFn: (studentNos: string[]) => employmentV2Api.batchDelete(studentNos),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employmentV2'] })
      setSelectedItems([])
      addToast({ title: '成功', description: '已软删除' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '删除失败', variant: 'destructive' }),
  })

  const restoreMutation = useMutation({
    mutationFn: (studentNos: string[]) => employmentV2Api.batchRestore(studentNos),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employmentV2'] })
      setSelectedItems([])
      addToast({ title: '成功', description: '已恢复' })
    },
    onError: (err: Error) => addToast({ title: '错误', description: err.message || '恢复失败', variant: 'destructive' }),
  })

  const canEdit = user ? PERMISSIONS.canEditEmployment(user.roles) : false
  const canDelete = user ? PERMISSIONS.canDeleteEmployment(user.roles) : false

  const toggleSelect = (studentNo: string) => {
    setSelectedItems((prev) =>
      prev.includes(studentNo) ? prev.filter((n) => n !== studentNo) : [...prev, studentNo]
    )
  }

  const openAdd = () => {
    setEditing(null)
    setFormData({})
    setIsOpen(true)
  }

  const openEdit = (emp: EmploymentV2) => {
    setEditing(emp)
    setFormData(emp)
    setIsOpen(true)
  }

  const handleSubmit = () => {
    if (editing) {
      updateMutation.mutate({ studentNo: editing.student_no, data: formData })
    } else {
      createMutation.mutate(formData as EmploymentV2)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">就业管理 v2</h2>
          <p className="text-muted-foreground">v2 版本就业信息管理（支持条件搜索、软删除、批量恢复）</p>
        </div>
        {canEdit && (
          <Button onClick={openAdd}>
            <Plus className="h-4 w-4 mr-2" />
            新增就业
          </Button>
        )}
      </div>

      <div className="flex gap-3 flex-wrap">
        <Input placeholder="公司" value={query.company || ''} onChange={(e) => setQuery({ ...query, company: e.target.value })} className="w-40" />
        <Input placeholder="岗位" value={query.position || ''} onChange={(e) => setQuery({ ...query, position: e.target.value })} className="w-40" />
        <Input placeholder="工作地点" value={query.work_location || ''} onChange={(e) => setQuery({ ...query, work_location: e.target.value })} className="w-40" />
        <Input type="number" placeholder="最低薪资" value={query.min_salary || ''} onChange={(e) => setQuery({ ...query, min_salary: Number(e.target.value) || undefined })} className="w-32" />
        <Input type="number" placeholder="最高薪资" value={query.max_salary || ''} onChange={(e) => setQuery({ ...query, max_salary: Number(e.target.value) || undefined })} className="w-32" />
        <Select value={String(query.employment_status ?? '')} onChange={(e) => setQuery({ ...query, employment_status: e.target.value ? Number(e.target.value) : undefined })} className="w-32">
          <option value="">全部状态</option>
          <option value="1">正常</option>
          <option value="0">已删除</option>
        </Select>
        <Button variant="outline" onClick={() => setQuery({})}>重置</Button>
      </div>

      {canDelete && selectedItems.length > 0 && (
        <div className="flex gap-2">
          <Button variant="destructive" size="sm" onClick={() => deleteMutation.mutate(selectedItems)}>
            <Trash2 className="h-4 w-4 mr-2" />
            批量软删除 ({selectedItems.length})
          </Button>
          <Button variant="outline" size="sm" onClick={() => restoreMutation.mutate(selectedItems)}>
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
                {canDelete && <TableHead className="w-12"><input type="checkbox" /></TableHead>}
                <TableHead>学号</TableHead>
                <TableHead>公司</TableHead>
                <TableHead>岗位</TableHead>
                <TableHead>薪资</TableHead>
                <TableHead>工作地点</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>已删除</TableHead>
                {(canEdit || canDelete) && <TableHead className="text-right">操作</TableHead>}
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow><TableCell colSpan={canDelete ? 9 : 8} className="text-center py-8">加载中...</TableCell></TableRow>
              ) : employments?.length === 0 ? (
                <TableRow><TableCell colSpan={canDelete ? 9 : 8} className="text-center py-8 text-muted-foreground">暂无数据</TableCell></TableRow>
              ) : (
                employments?.map((emp) => (
                  <TableRow key={emp.student_no}>
                    {canDelete && (
                      <TableCell>
                        <input type="checkbox" checked={selectedItems.includes(emp.student_no)} onChange={() => toggleSelect(emp.student_no)} />
                      </TableCell>
                    )}
                    <TableCell>{emp.student_no}</TableCell>
                    <TableCell className="font-medium">{emp.company}</TableCell>
                    <TableCell>{emp.position}</TableCell>
                    <TableCell>{emp.salary}</TableCell>
                    <TableCell>{emp.work_location}</TableCell>
                    <TableCell>{EMPLOYMENT_STATUS_MAP[emp.employment_status]}</TableCell>
                    <TableCell>{emp.is_deleted ? '是' : '否'}</TableCell>
                    {(canEdit || canDelete) && (
                      <TableCell className="text-right">
                        {canEdit && (
                          <Button variant="ghost" size="sm" onClick={() => openEdit(emp)}>
                            <Pencil className="h-4 w-4" />
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
