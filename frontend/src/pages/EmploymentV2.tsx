import { useState, useMemo } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { employmentV2Api, type EmploymentQuery } from '@/api/employmentV2'
import { studentApi } from '@/api/students'
import { useAuthStore } from '@/stores/authStore'
import { PERMISSIONS } from '@/lib/constants'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { useToast } from '@/components/ui/toast'
import {
  Plus,
  Trash2,
  Pencil,
  Search,
  Briefcase,
  MapPin,
  Banknote,
  User,
  X,
  GraduationCap,
  CalendarDays,
} from 'lucide-react'
import type { EmploymentV2 } from '@/types'

const STATUS_OPTIONS = [
  { value: '', label: '全部状态' },
  { value: '待业', label: '待业' },
  { value: '在聘', label: '在聘' },
  { value: '已离职', label: '已离职' },
] as const

const STATUS_BADGE: Record<string, { variant: 'default' | 'secondary' | 'destructive' | 'outline'; label: string }> = {
  '待业': { variant: 'secondary', label: '待业' },
  '在聘': { variant: 'default', label: '在聘' },
  '已离职': { variant: 'destructive', label: '已离职' },
}

export default function EmploymentV2Page() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const { addToast } = useToast()

  const [query, setQuery] = useState<EmploymentQuery>({})
  const [selectedItems, setSelectedItems] = useState<string[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const [editing, setEditing] = useState<EmploymentV2 | null>(null)
  const [formData, setFormData] = useState<Partial<EmploymentV2>>({})
  const [detailOpen, setDetailOpen] = useState(false)
  const [detailStudentNo, setDetailStudentNo] = useState<string | null>(null)

  const canEdit = user ? PERMISSIONS.canEditEmployment(user.roles) : false
  const canDelete = user ? PERMISSIONS.canDeleteEmployment(user.roles) : false

  const { data: students } = useQuery({
    queryKey: ['students', 'all'],
    queryFn: () => studentApi.getAll().then((r) => r.data),
  })

  const { data: rawEmployments, isLoading } = useQuery({
    queryKey: ['employmentV2', query],
    queryFn: () => employmentV2Api.search(query).then((r) => r.data),
  })

  const employments = rawEmployments ?? []

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

  const toggleSelect = (studentNo: string) => {
    setSelectedItems((prev) =>
      prev.includes(studentNo) ? prev.filter((n) => n !== studentNo) : [...prev, studentNo]
    )
  }

  const selectAll = () => {
    if (selectedItems.length === employments.length) {
      setSelectedItems([])
    } else {
      setSelectedItems(employments.map((e) => e.student_no))
    }
  }

  const openAdd = () => {
    setEditing(null)
    setFormData({ employment_status: '在聘' })
    setIsOpen(true)
  }

  const openEdit = (emp: EmploymentV2) => {
    setEditing(emp)
    setFormData(emp)
    setIsOpen(true)
  }

  const openDetail = (studentNo: string) => {
    setDetailStudentNo(studentNo)
    setDetailOpen(true)
  }

  const handleSubmit = () => {
    if (editing) {
      updateMutation.mutate({ studentNo: editing.student_no, data: formData })
    } else {
      createMutation.mutate(formData as EmploymentV2)
    }
  }

  const detailEmp = useMemo(() => {
    if (!detailStudentNo || !rawEmployments) return null
    return rawEmployments.find((e) => e.student_no === detailStudentNo) || null
  }, [detailStudentNo, rawEmployments])

  const detailStudent = useMemo(() => {
    if (!detailStudentNo || !students) return null
    return students.find((s) => s.student_no === detailStudentNo) || null
  }, [detailStudentNo, students])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">就业管理 v2</h2>
          <p className="text-muted-foreground">就业信息全生命周期管理（搜索、编辑、软删除、恢复）</p>
        </div>
        {canEdit && (
          <Button onClick={openAdd}>
            <Plus className="h-4 w-4 mr-2" />
            新增就业
          </Button>
        )}
      </div>

      {/* Search & Filter */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap items-end gap-3">
            <div className="space-y-1">
              <label className="text-xs font-medium text-muted-foreground">公司</label>
              <Input placeholder="搜索公司" value={query.company_name || ''} onChange={(e) => setQuery({ ...query, company_name: e.target.value || undefined })} className="w-40" />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-muted-foreground">岗位</label>
              <Input placeholder="搜索岗位" value={query.position || ''} onChange={(e) => setQuery({ ...query, position: e.target.value || undefined })} className="w-40" />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-muted-foreground">工作地点</label>
              <Input placeholder="搜索地点" value={query.work_location || ''} onChange={(e) => setQuery({ ...query, work_location: e.target.value || undefined })} className="w-40" />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-muted-foreground">最低薪资</label>
              <Input type="number" placeholder="最低薪资" value={query.min_salary || ''} onChange={(e) => setQuery({ ...query, min_salary: Number(e.target.value) || undefined })} className="w-32" />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-muted-foreground">最高薪资</label>
              <Input type="number" placeholder="最高薪资" value={query.max_salary || ''} onChange={(e) => setQuery({ ...query, max_salary: Number(e.target.value) || undefined })} className="w-32" />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-medium text-muted-foreground">就业状态</label>
              <Select value={query.employment_status ?? ''} onChange={(e) => setQuery({ ...query, employment_status: e.target.value || undefined })} className="w-32">
                {STATUS_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </Select>
            </div>
            <Button variant="outline" onClick={() => setQuery({})} className="mb-0.5">
              <X className="h-4 w-4 mr-1" />
              重置
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <div className="flex items-center justify-end">
        {canDelete && selectedItems.length > 0 && (
          <Button variant="destructive" size="sm" onClick={() => deleteMutation.mutate(selectedItems)}>
            <Trash2 className="h-4 w-4 mr-2" />
            软删除 ({selectedItems.length})
          </Button>
        )}
      </div>

      <DataTable
        data={employments}
        isLoading={isLoading}
        canEdit={canEdit}
        canDelete={canDelete}
        selectedItems={selectedItems}
        toggleSelect={toggleSelect}
        selectAll={selectAll}
        onEdit={openEdit}
        onDetail={openDetail}
      />

      {/* Add / Edit Dialog */}
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>{editing ? '编辑就业信息' : '新增就业信息'}</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">学生 <span className="text-destructive">*</span></label>
              <Select value={formData.student_no || ''} onChange={(e) => setFormData({ ...formData, student_no: e.target.value })} disabled={!!editing}>
                <option value="">请选择学生</option>
                {students?.map((s) => (
                  <option key={s.student_no} value={s.student_no}>{s.name} ({s.student_no})</option>
                ))}
              </Select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">公司 <span className="text-destructive">*</span></label>
                <Input value={formData.company_name || ''} onChange={(e) => setFormData({ ...formData, company_name: e.target.value })} placeholder="公司名称" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">岗位</label>
                <Input value={formData.position || ''} onChange={(e) => setFormData({ ...formData, position: e.target.value })} placeholder="工作岗位" />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">薪资 <span className="text-destructive">*</span></label>
                <Input type="number" value={formData.salary || ''} onChange={(e) => setFormData({ ...formData, salary: Number(e.target.value) })} placeholder="月薪" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">工作地点</label>
                <Input value={formData.work_location || ''} onChange={(e) => setFormData({ ...formData, work_location: e.target.value })} placeholder="城市/地区" />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">就业开放时间</label>
                <Input type="datetime-local" value={formData.employment_open_time || ''} onChange={(e) => setFormData({ ...formData, employment_open_time: e.target.value })} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Offer 时间</label>
                <Input type="datetime-local" value={formData.offer_time || ''} onChange={(e) => setFormData({ ...formData, offer_time: e.target.value })} />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">就业状态</label>
              <Select value={formData.employment_status || ''} onChange={(e) => setFormData({ ...formData, employment_status: e.target.value })}>
                {STATUS_OPTIONS.filter((o) => o.value).map((opt) => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsOpen(false)}>取消</Button>
            <Button onClick={handleSubmit} disabled={!formData.student_no || !formData.company_name || !formData.salary}>
              {editing ? '保存修改' : '确认添加'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Detail Dialog */}
      <Dialog open={detailOpen} onOpenChange={setDetailOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>就业详情</DialogTitle>
          </DialogHeader>
          {detailEmp && (
            <div className="space-y-4 py-2">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <User className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <div className="font-semibold">{detailStudent?.name || detailEmp.student_no}</div>
                  <div className="text-sm text-muted-foreground">{detailEmp.student_no}</div>
                </div>
                <Badge variant={STATUS_BADGE[detailEmp.employment_status]?.variant || 'outline'}>
                  {STATUS_BADGE[detailEmp.employment_status]?.label || detailEmp.employment_status}
                </Badge>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="flex items-start gap-2">
                  <Briefcase className="h-4 w-4 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-muted-foreground">公司</div>
                    <div className="font-medium">{detailEmp.company_name || '-'}</div>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <GraduationCap className="h-4 w-4 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-muted-foreground">岗位</div>
                    <div className="font-medium">{detailEmp.position || '-'}</div>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <Banknote className="h-4 w-4 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-muted-foreground">薪资</div>
                    <div className="font-medium">{detailEmp.salary}</div>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-muted-foreground">工作地点</div>
                    <div className="font-medium">{detailEmp.work_location || '-'}</div>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <CalendarDays className="h-4 w-4 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-muted-foreground">就业开放时间</div>
                    <div className="font-medium">{detailEmp.employment_open_time || '-'}</div>
                  </div>
                </div>
                <div className="flex items-start gap-2">
                  <CalendarDays className="h-4 w-4 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-muted-foreground">Offer 时间</div>
                    <div className="font-medium">{detailEmp.offer_time || '-'}</div>
                  </div>
                </div>
              </div>

              {detailStudent && (
                <div className="rounded-lg bg-muted p-3 text-sm space-y-1">
                  <div className="text-muted-foreground">学生信息</div>
                  <div>班级：{detailStudent.class_no}</div>
                  <div>性别：{detailStudent.gender}</div>
                  <div>电话：{detailStudent.phone}</div>
                </div>
              )}
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setDetailOpen(false)}>关闭</Button>
            {canEdit && detailEmp && (
              <Button onClick={() => { setDetailOpen(false); openEdit(detailEmp) }}>
                <Pencil className="h-4 w-4 mr-2" />
                编辑
              </Button>
            )}
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

/* ---------------- DataTable Component ---------------- */

interface DataTableProps {
  data: EmploymentV2[]
  isLoading: boolean
  canEdit: boolean
  canDelete: boolean
  selectedItems: string[]
  toggleSelect: (studentNo: string) => void
  selectAll: () => void
  onEdit: (emp: EmploymentV2) => void
  onDetail: (studentNo: string) => void
}

function DataTable({ data, isLoading, canEdit, canDelete, selectedItems, toggleSelect, selectAll, onEdit, onDetail }: DataTableProps) {
  const allSelected = data.length > 0 && selectedItems.length === data.length

  return (
    <div className="border rounded-lg overflow-hidden">
      <div className="max-h-[600px] overflow-auto">
        <Table>
          <TableHeader>
            <TableRow>
              {canDelete && (
                <TableHead className="w-12">
                  <input type="checkbox" checked={allSelected} onChange={selectAll} />
                </TableHead>
              )}
              <TableHead>学号</TableHead>
              <TableHead>公司</TableHead>
              <TableHead>岗位</TableHead>
              <TableHead>薪资</TableHead>
              <TableHead>工作地点</TableHead>
              <TableHead>状态</TableHead>
              <TableHead className="text-right">操作</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={canDelete ? 8 : 7} className="text-center py-8">
                  <div className="flex items-center justify-center gap-2 text-muted-foreground">
                    <Search className="h-4 w-4 animate-spin" />
                    加载中...
                  </div>
                </TableCell>
              </TableRow>
            ) : data.length === 0 ? (
              <TableRow>
                <TableCell colSpan={canDelete ? 8 : 7} className="text-center py-8 text-muted-foreground">
                  暂无数据
                </TableCell>
              </TableRow>
            ) : (
              data.map((emp) => (
                <TableRow key={emp.student_no} className="cursor-pointer hover:bg-muted/50" onClick={() => onDetail(emp.student_no)}>
                  {canDelete && (
                    <TableCell onClick={(e) => e.stopPropagation()}>
                      <input type="checkbox" checked={selectedItems.includes(emp.student_no)} onChange={() => toggleSelect(emp.student_no)} />
                    </TableCell>
                  )}
                  <TableCell className="font-medium">{emp.student_no}</TableCell>
                  <TableCell>{emp.company_name}</TableCell>
                  <TableCell>{emp.position || '-'}</TableCell>
                  <TableCell>{emp.salary}</TableCell>
                  <TableCell>{emp.work_location || '-'}</TableCell>
                  <TableCell>
                    <Badge variant={STATUS_BADGE[emp.employment_status]?.variant || 'outline'}>
                      {STATUS_BADGE[emp.employment_status]?.label || emp.employment_status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right" onClick={(e) => e.stopPropagation()}>
                    {canEdit && (
                      <Button variant="ghost" size="sm" onClick={() => onEdit(emp)}>
                        <Pencil className="h-4 w-4" />
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
