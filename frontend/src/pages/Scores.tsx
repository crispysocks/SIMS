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
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/components/ui/toast'
import { Plus, Trash2, Pencil, Search, Trophy, FileBarChart } from 'lucide-react'
import type { Score, ExamRankingItem, ClassScoreReportItem } from '@/types'

type TabValue = 'all' | 'student' | 'ranking' | 'report'

export default function ScoresPage() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const { addToast } = useToast()

  const [activeTab, setActiveTab] = useState<TabValue>('all')
  const [searchStudentNo, setSearchStudentNo] = useState('')
  const [rankingExamNo, setRankingExamNo] = useState('')
  const [reportExamNo, setReportExamNo] = useState('')

  const [isOpen, setIsOpen] = useState(false)
  const [editing, setEditing] = useState<Score | null>(null)
  const [formData, setFormData] = useState<Partial<Score>>({})

  const { data: students } = useQuery({
    queryKey: ['students', 'all'],
    queryFn: () => studentApi.getAll().then((r) => r.data),
  })

  const { data: allScores, isLoading: allLoading } = useQuery({
    queryKey: ['scores', 'all'],
    queryFn: () => scoreApi.getAll().then((r) => r.data),
    enabled: activeTab === 'all',
  })

  const { data: studentScores, isLoading: studentLoading } = useQuery({
    queryKey: ['scores', 'student', searchStudentNo],
    queryFn: () => scoreApi.getByStudent(searchStudentNo).then((r) => r.data),
    enabled: activeTab === 'student' && !!searchStudentNo,
  })

  const { data: rankingData, isLoading: rankingLoading } = useQuery({
    queryKey: ['scores', 'ranking', rankingExamNo],
    queryFn: () => scoreApi.examRanking(Number(rankingExamNo)).then((r) => r.data),
    enabled: activeTab === 'ranking' && !!rankingExamNo,
  })

  const { data: reportData, isLoading: reportLoading } = useQuery({
    queryKey: ['scores', 'report', reportExamNo],
    queryFn: () => scoreApi.classScoreReport(Number(reportExamNo)).then((r) => r.data),
    enabled: activeTab === 'report' && !!reportExamNo,
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
    mutationFn: (data: { student_no: string; exam_no: string }) => scoreApi.delete(data),
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

  const renderScoreTable = (scores: Score[] | undefined, loading: boolean, showActions = true) => (
    <div className="border rounded-lg overflow-hidden">
      <div className="max-h-[600px] overflow-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>学号</TableHead>
              <TableHead>考试编号</TableHead>
              <TableHead>成绩</TableHead>
              <TableHead>考试日期</TableHead>
              {showActions && (canEdit || canDelete) && <TableHead className="text-right">操作</TableHead>}
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={showActions && (canEdit || canDelete) ? 5 : 4} className="text-center py-8">加载中...</TableCell>
              </TableRow>
            ) : !scores || scores.length === 0 ? (
              <TableRow>
                <TableCell colSpan={showActions && (canEdit || canDelete) ? 5 : 4} className="text-center py-8 text-muted-foreground">暂无成绩记录</TableCell>
              </TableRow>
            ) : (
              scores.map((score) => (
                <TableRow key={`${score.student_no}-${score.exam_no}`}>
                  <TableCell>{score.student_no}</TableCell>
                  <TableCell>{score.exam_no}</TableCell>
                  <TableCell>
                    <Badge variant={score.score >= 60 ? 'default' : 'destructive'}>
                      {score.score}
                    </Badge>
                  </TableCell>
                  <TableCell>{score.exam_date || '-'}</TableCell>
                  {showActions && (canEdit || canDelete) && (
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
  )

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">成绩管理</h2>
          <p className="text-muted-foreground">查询、录入和管理学生成绩</p>
        </div>
        {canEdit && (
          <Button onClick={openAdd}>
            <Plus className="h-4 w-4 mr-2" />
            录入成绩
          </Button>
        )}
      </div>

      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as TabValue)}>
        <TabsList className="flex-wrap h-auto">
          <TabsTrigger value="all">全部成绩</TabsTrigger>
          <TabsTrigger value="student">按学生查询</TabsTrigger>
          <TabsTrigger value="ranking">
            <Trophy className="h-3.5 w-3.5 mr-1" />
            考试排名
          </TabsTrigger>
          <TabsTrigger value="report">
            <FileBarChart className="h-3.5 w-3.5 mr-1" />
            班级报表
          </TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {renderScoreTable(allScores, allLoading)}
        </TabsContent>

        <TabsContent value="student" className="space-y-4">
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
          {renderScoreTable(studentScores, studentLoading)}
        </TabsContent>

        <TabsContent value="ranking" className="space-y-4">
          <div className="flex gap-3">
            <Input
              placeholder="考试编号"
              value={rankingExamNo}
              onChange={(e) => setRankingExamNo(e.target.value)}
              className="max-w-[140px]"
            />
          </div>
          <div className="border rounded-lg overflow-hidden">
            <div className="max-h-[600px] overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>排名</TableHead>
                    <TableHead>学号</TableHead>
                    <TableHead>姓名</TableHead>
                    <TableHead>班级</TableHead>
                    <TableHead>成绩</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rankingLoading ? (
                    <TableRow><TableCell colSpan={5} className="text-center py-8">加载中...</TableCell></TableRow>
                  ) : !rankingData || rankingData.length === 0 ? (
                    <TableRow><TableCell colSpan={5} className="text-center py-8 text-muted-foreground">请输入考试编号查询排名</TableCell></TableRow>
                  ) : (
                    rankingData.map((item: ExamRankingItem) => (
                      <TableRow key={`${item.student_no}-${item.rank}`}>
                        <TableCell>
                          <Badge variant={item.rank <= 3 ? 'default' : 'secondary'}>{item.rank}</Badge>
                        </TableCell>
                        <TableCell>{item.student_no}</TableCell>
                        <TableCell>{item.student_name}</TableCell>
                        <TableCell>{item.class_name}</TableCell>
                        <TableCell>{item.score}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="report" className="space-y-4">
          <div className="flex gap-3">
            <Input
              placeholder="考试编号"
              value={reportExamNo}
              onChange={(e) => setReportExamNo(e.target.value)}
              className="max-w-[140px]"
            />
          </div>
          <div className="border rounded-lg overflow-hidden">
            <div className="max-h-[600px] overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>班级编号</TableHead>
                    <TableHead>班级名称</TableHead>
                    <TableHead>考试编号</TableHead>
                    <TableHead>人数</TableHead>
                    <TableHead>平均分</TableHead>
                    <TableHead>优秀率</TableHead>
                    <TableHead>及格率</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {reportLoading ? (
                    <TableRow><TableCell colSpan={7} className="text-center py-8">加载中...</TableCell></TableRow>
                  ) : !reportData || reportData.length === 0 ? (
                    <TableRow><TableCell colSpan={7} className="text-center py-8 text-muted-foreground">请输入考试编号查询报表</TableCell></TableRow>
                  ) : (
                    reportData.map((item: ClassScoreReportItem) => (
                      <TableRow key={`${item.class_no}-${item.exam_no}`}>
                        <TableCell>{item.class_no}</TableCell>
                        <TableCell>{item.class_name}</TableCell>
                        <TableCell>{item.exam_no}</TableCell>
                        <TableCell>{item.student_count}</TableCell>
                        <TableCell>{item.avg_score.toFixed(2)}</TableCell>
                        <TableCell>{(item.excellent_rate * 100).toFixed(1)}%</TableCell>
                        <TableCell>{(item.pass_rate * 100).toFixed(1)}%</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          </div>
        </TabsContent>
      </Tabs>

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
                <label className="text-sm font-medium">成绩</label>
                <Input type="number" value={formData.score || ''} onChange={(e) => setFormData({ ...formData, score: Number(e.target.value) })} />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">考试日期</label>
              <Input type="date" value={formData.exam_date || ''} onChange={(e) => setFormData({ ...formData, exam_date: e.target.value })} />
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
