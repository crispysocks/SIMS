import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { teacherApi } from '@/api/teachers'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Search, PieChart } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function TeacherSearchPage() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [gender, setGender] = useState('')
  const [searchParams, setSearchParams] = useState<{ name?: string; gender?: string }>({})

  const { data: teachers, isLoading } = useQuery({
    queryKey: ['teachers', 'search', searchParams],
    queryFn: () => teacherApi.search(searchParams).then((r) => r.data),
    enabled: Object.keys(searchParams).length > 0,
  })

  const handleSearch = () => {
    const params: { name?: string; gender?: string } = {}
    if (name.trim()) params.name = name.trim()
    if (gender) params.gender = gender
    setSearchParams(params)
  }

  const handleReset = () => {
    setName('')
    setGender('')
    setSearchParams({})
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">教师查询</h2>
          <p className="text-muted-foreground">按姓名或性别搜索教师</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/teachers/stats')}>
          <PieChart className="h-4 w-4 mr-2" />
          性别统计
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>搜索条件</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3 items-end">
            <div className="space-y-2">
              <label className="text-sm font-medium">姓名</label>
              <Input
                placeholder="支持模糊查询"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-48"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">性别</label>
              <select
                className="flex h-9 w-32 rounded-md border border-input bg-transparent px-3 py-1 text-sm"
                value={gender}
                onChange={(e) => setGender(e.target.value)}
              >
                <option value="">全部</option>
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
            <Button onClick={handleSearch}>
              <Search className="h-4 w-4 mr-2" />
              查询
            </Button>
            <Button variant="outline" onClick={handleReset}>
              重置
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>查询结果</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="max-h-[500px] overflow-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>教师编号</TableHead>
                  <TableHead>姓名</TableHead>
                  <TableHead>性别</TableHead>
                  <TableHead>电话</TableHead>
                  <TableHead>邮箱</TableHead>
                  <TableHead>授课科目</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8">
                      加载中...
                    </TableCell>
                  </TableRow>
                ) : Object.keys(searchParams).length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                      请输入搜索条件并点击查询
                    </TableCell>
                  </TableRow>
                ) : teachers?.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                      未找到符合条件的教师
                    </TableCell>
                  </TableRow>
                ) : (
                  teachers?.map((teacher) => (
                    <TableRow key={teacher.teacher_no}>
                      <TableCell>{teacher.teacher_no}</TableCell>
                      <TableCell className="font-medium">{teacher.name}</TableCell>
                      <TableCell>{teacher.gender}</TableCell>
                      <TableCell>{teacher.phone || '-'}</TableCell>
                      <TableCell>{teacher.email || '-'}</TableCell>
                      <TableCell>{teacher.subject || '-'}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
