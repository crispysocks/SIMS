import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { statisticsApi } from '@/api/statistics'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function StatisticsPage() {
  const [age, setAge] = useState('30')
  const [score, setScore] = useState('80')
  const [activeTab, setActiveTab] = useState('class-gender')

  const { data: ageFilterData } = useQuery({
    queryKey: ['statistics', 'age-filter', age],
    queryFn: () => statisticsApi.ageFilter(Number(age)).then((r) => r.data),
    enabled: activeTab === 'age-filter',
  })

  const { data: classGenderData } = useQuery({
    queryKey: ['statistics', 'class-gender'],
    queryFn: () => statisticsApi.classGender().then((r) => r.data),
    enabled: activeTab === 'class-gender',
  })

  const { data: alwaysAboveData } = useQuery({
    queryKey: ['statistics', 'always-above', score],
    queryFn: () => statisticsApi.alwaysAbove(Number(score)).then((r) => r.data),
    enabled: activeTab === 'always-above',
  })

  const { data: failedTwiceData } = useQuery({
    queryKey: ['statistics', 'failed-twice'],
    queryFn: () => statisticsApi.failedTwice().then((r) => r.data),
    enabled: activeTab === 'failed-twice',
  })

  const { data: classAvgScoreData } = useQuery({
    queryKey: ['statistics', 'class-avg-score'],
    queryFn: () => statisticsApi.classAvgScore().then((r) => r.data),
    enabled: activeTab === 'class-avg-score',
  })

  const { data: topSalaryData } = useQuery({
    queryKey: ['statistics', 'top-salary'],
    queryFn: () => statisticsApi.topSalary().then((r) => r.data),
    enabled: activeTab === 'top-salary',
  })

  const { data: studentDurationData } = useQuery({
    queryKey: ['statistics', 'student-offer-duration'],
    queryFn: () => statisticsApi.studentOfferDuration().then((r) => r.data),
    enabled: activeTab === 'student-offer-duration',
  })

  const { data: classDurationData } = useQuery({
    queryKey: ['statistics', 'class-offer-duration'],
    queryFn: () => statisticsApi.classOfferDuration().then((r) => r.data),
    enabled: activeTab === 'class-offer-duration',
  })

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">统计分析</h2>
        <p className="text-muted-foreground">查看各类数据统计报表</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="flex-wrap h-auto">
          <TabsTrigger value="class-gender">班级性别</TabsTrigger>
          <TabsTrigger value="class-avg-score">班级平均分</TabsTrigger>
          <TabsTrigger value="top-salary">高薪排名</TabsTrigger>
          <TabsTrigger value="age-filter">年龄筛选</TabsTrigger>
          <TabsTrigger value="always-above">高分学生</TabsTrigger>
          <TabsTrigger value="failed-twice">不及格学生</TabsTrigger>
          <TabsTrigger value="student-offer-duration">就业时长</TabsTrigger>
          <TabsTrigger value="class-offer-duration">班级就业时长</TabsTrigger>
        </TabsList>

        <TabsContent value="class-gender">
          <Card>
            <CardHeader>
              <CardTitle>班级性别统计</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={classGenderData || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="class_name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="male_count" name="男生" fill="#3b82f6" />
                    <Bar dataKey="female_count" name="女生" fill="#ec4899" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="class-avg-score">
          <Card>
            <CardHeader>
              <CardTitle>班级平均分</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={classAvgScoreData || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="class_name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="avg_score" name="平均分" fill="#10b981" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="top-salary">
          <Card>
            <CardHeader>
              <CardTitle>高薪学生 TOP</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="max-h-[500px] overflow-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>学号</TableHead>
                      <TableHead>姓名</TableHead>
                      <TableHead>班级</TableHead>
                      <TableHead>薪资</TableHead>
                      <TableHead>公司</TableHead>
                      <TableHead>岗位</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {topSalaryData?.map((item) => (
                      <TableRow key={item.student_no}>
                        <TableCell>{item.student_no}</TableCell>
                        <TableCell className="font-medium">{item.name}</TableCell>
                        <TableCell>{item.class_no}</TableCell>
                        <TableCell className="text-green-600 font-medium">{item.salary}</TableCell>
                        <TableCell>{item.company}</TableCell>
                        <TableCell>{item.position}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="age-filter">
          <Card>
            <CardHeader>
              <CardTitle>年龄筛选</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-3 mb-4">
                <Input type="number" placeholder="年龄" value={age} onChange={(e) => setAge(e.target.value)} className="w-32" />
                <Button onClick={() => setAge(age)}>查询</Button>
              </div>
              <div className="max-h-[500px] overflow-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>学号</TableHead>
                      <TableHead>姓名</TableHead>
                      <TableHead>性别</TableHead>
                      <TableHead>年龄</TableHead>
                      <TableHead>班级</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {ageFilterData?.map((student) => (
                      <TableRow key={student.student_no}>
                        <TableCell>{student.student_no}</TableCell>
                        <TableCell>{student.name}</TableCell>
                        <TableCell>{student.gender}</TableCell>
                        <TableCell>{student.age}</TableCell>
                        <TableCell>{student.class_no}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="always-above">
          <Card>
            <CardHeader>
              <CardTitle>每次考试高于指定分数</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-3 mb-4">
                <Input type="number" placeholder="分数" value={score} onChange={(e) => setScore(e.target.value)} className="w-32" />
                <Button onClick={() => setScore(score)}>查询</Button>
              </div>
              <div className="max-h-[500px] overflow-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>学号</TableHead>
                      <TableHead>姓名</TableHead>
                      <TableHead>班级</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {alwaysAboveData?.map((student) => (
                      <TableRow key={student.student_no}>
                        <TableCell>{student.student_no}</TableCell>
                        <TableCell>{student.name}</TableCell>
                        <TableCell>{student.class_no}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="failed-twice">
          <Card>
            <CardHeader>
              <CardTitle>两次及以上不及格学生</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="max-h-[500px] overflow-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>学号</TableHead>
                      <TableHead>姓名</TableHead>
                      <TableHead>班级</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {failedTwiceData?.map((student) => (
                      <TableRow key={student.student_no}>
                        <TableCell>{student.student_no}</TableCell>
                        <TableCell>{student.name}</TableCell>
                        <TableCell>{student.class_no}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="student-offer-duration">
          <Card>
            <CardHeader>
              <CardTitle>个人就业时长（天）</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="max-h-[500px] overflow-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>学号</TableHead>
                      <TableHead>姓名</TableHead>
                      <TableHead>就业时长（天）</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {studentDurationData?.map((item) => (
                      <TableRow key={item.student_no}>
                        <TableCell>{item.student_no}</TableCell>
                        <TableCell>{item.name}</TableCell>
                        <TableCell>{item.offer_duration_days}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="class-offer-duration">
          <Card>
            <CardHeader>
              <CardTitle>班级平均就业时长（天）</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={classDurationData || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="class_name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="avg_offer_duration_days" name="平均就业时长（天）" fill="#8b5cf6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
