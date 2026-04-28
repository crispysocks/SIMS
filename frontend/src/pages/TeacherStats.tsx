import { useQuery } from '@tanstack/react-query'
import { teacherApi } from '@/api/teachers'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const COLORS = ['#3b82f6', '#ec4899']

export default function TeacherStatsPage() {
  const navigate = useNavigate()

  const { data: stats, isLoading } = useQuery({
    queryKey: ['teachers', 'gender-stats'],
    queryFn: () => teacherApi.genderStats().then((r) => r.data),
  })

  const chartData =
    stats?.map((item) => ({
      name: item.gender,
      value: item.count,
    })) || []

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">教师性别统计</h2>
          <p className="text-muted-foreground">按性别分组统计教师数量及比例</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/teachers/search')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          返回查询
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>饼状图</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[400px]">
              {isLoading ? (
                <div className="h-full flex items-center justify-center text-muted-foreground">
                  加载中...
                </div>
              ) : chartData.length === 0 ? (
                <div className="h-full flex items-center justify-center text-muted-foreground">
                  暂无数据
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={chartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${((percent ?? 0) * 100).toFixed(1)}%`}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {chartData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(value, name) => [value, name]}
                    />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>数据明细</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="max-h-[400px] overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>性别</TableHead>
                    <TableHead>数量</TableHead>
                    <TableHead>比例</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {isLoading ? (
                    <TableRow>
                      <TableCell colSpan={3} className="text-center py-8">
                        加载中...
                      </TableCell>
                    </TableRow>
                  ) : stats?.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={3} className="text-center py-8 text-muted-foreground">
                        暂无数据
                      </TableCell>
                    </TableRow>
                  ) : (
                    stats?.map((item) => (
                      <TableRow key={item.gender}>
                        <TableCell className="font-medium">{item.gender}</TableCell>
                        <TableCell>{item.count}</TableCell>
                        <TableCell>{(item.ratio * 100).toFixed(2)}%</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
