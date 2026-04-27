import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { studentApi } from '@/api/students'
import { scoreApi } from '@/api/scores'
import { employmentApi } from '@/api/employment'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { GENDER_MAP, EMPLOYMENT_STATUS_MAP } from '@/lib/constants'

export default function StudentDetailPage() {
  const { student_no } = useParams<{ student_no: string }>()
  const [activeTab, setActiveTab] = useState('info')

  const { data: student } = useQuery({
    queryKey: ['students', student_no],
    queryFn: () => studentApi.getById(student_no!).then((r) => r.data),
    enabled: !!student_no,
  })

  const { data: scores } = useQuery({
    queryKey: ['scores', student_no],
    queryFn: () => scoreApi.getByStudent(student_no!).then((r) => r.data),
    enabled: !!student_no,
  })

  const { data: employment } = useQuery({
    queryKey: ['employment', student_no],
    queryFn: () => employmentApi.getByStudent(student_no!).then((r) => r.data),
    enabled: !!student_no,
  })

  if (!student) return <div className="py-8 text-center">加载中...</div>

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{student.name}</h2>
        <p className="text-muted-foreground">学号: {student.student_no}</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="info">基本信息</TabsTrigger>
          <TabsTrigger value="scores">成绩记录</TabsTrigger>
          <TabsTrigger value="employment">就业信息</TabsTrigger>
        </TabsList>

        <TabsContent value="info">
          <Card>
            <CardHeader>
              <CardTitle>基本信息</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <InfoItem label="姓名" value={student.name} />
                <InfoItem label="学号" value={student.student_no} />
                <InfoItem label="性别" value={GENDER_MAP[student.gender] || student.gender} />
                <InfoItem label="班级" value={student.class_no} />
                <InfoItem label="年龄" value={String(student.age)} />
                <InfoItem label="电话" value={student.phone} />
                <InfoItem label="籍贯" value={student.native_place} />
                <InfoItem label="毕业院校" value={student.graduation_school} />
                <InfoItem label="专业" value={student.major} />
                <InfoItem label="学历" value={student.education_level} />
                <InfoItem label="顾问" value={student.consultant} />
                <InfoItem label="身份证" value={student.id_card} />
                <InfoItem label="入学时间" value={student.enrollment_time} />
                <InfoItem label="毕业时间" value={student.graduation_time} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="scores">
          <Card>
            <CardHeader>
              <CardTitle>成绩记录</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="max-h-[400px] overflow-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>考试编号</TableHead>
                      <TableHead>考试名称</TableHead>
                      <TableHead>成绩</TableHead>
                      <TableHead>考试日期</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {scores?.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center py-8 text-muted-foreground">暂无成绩记录</TableCell>
                      </TableRow>
                    ) : (
                      scores?.map((score) => (
                        <TableRow key={`${score.exam_no}-${score.exam_name}`}>
                          <TableCell>{score.exam_no}</TableCell>
                          <TableCell>{score.exam_name}</TableCell>
                          <TableCell>
                            <Badge variant={score.score >= 60 ? 'default' : 'destructive'}>
                              {score.score}
                            </Badge>
                          </TableCell>
                          <TableCell>{score.exam_date}</TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="employment">
          <Card>
            <CardHeader>
              <CardTitle>就业信息</CardTitle>
            </CardHeader>
            <CardContent>
              {employment ? (
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <InfoItem label="就业状态" value={EMPLOYMENT_STATUS_MAP[employment.employment_status] || String(employment.employment_status)} />
                  <InfoItem label="公司" value={employment.company} />
                  <InfoItem label="岗位" value={employment.position} />
                  <InfoItem label="薪资" value={`${employment.salary}`} />
                  <InfoItem label="工作地点" value={employment.work_location} />
                  <InfoItem label="开放时间" value={employment.employment_open_time} />
                  <InfoItem label="Offer时间" value={employment.offer_time} />
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">暂无就业信息</div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

function InfoItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-sm text-muted-foreground">{label}</div>
      <div className="text-sm font-medium">{value || '-'}</div>
    </div>
  )
}
