export interface Student {
  student_no: string
  name: string
  gender: string
  grade: string
  phone: string
  email: string
  id_card: string
  entrance_time: string
  graduate_time: string
  class_no: string
  isdeleted: number
  age: number
  birth_place: string
  graduate_school: string
  major: string
  education: string
  advisor_name: string
}

export interface Teacher {
  teacher_no: string
  name: string
  gender: string
  phone: string
  email: string
  id_card: string
  birthday: string
  hire_date: string
  subject: string
  isdeleted: number
}

export interface ClassInfo {
  class_no: string
  class_name: string
  class_open_time: string
  head_teacher_no: string
  instructor_no: string
  description: string
}

export interface Score {
  student_no: string
  exam_no: string
  score: number
  exam_date: string
}

export interface Employment {
  student_no: string
  employment_status: number
  employment_open_time: string
  offer_time: string
  company: string
  salary: number
  position: string
  work_location: string
}

export interface EmploymentV2 {
  student_no: string
  employment_status: string
  employment_open_time: string
  offer_time: string
  company_name: string
  salary: number
  position: string
  work_location: string
  isdeleted: number
}

export interface User {
  username: string
  roles: string[]
}

export interface ClassGenderStats {
  class_name: string
  male_count: number
  female_count: number
}

export interface ClassGenderStat {
  class_name: string
  male_count: number
  female_count: number
}

export interface TeacherGenderStat {
  gender: string
  count: number
  ratio: number
}

export interface TopSalaryStudent {
  student_no: string
  name: string
  class_no: string
  company: string
  salary: number
  position: string
}

export interface AvgSalaryByGroup {
  group_key: string
  avg_salary: number
}

export interface AgeFilterResult {
  student_no: string
  name: string
  age: number
}

export interface AlwaysAboveResult {
  student_no: string
  name: string
  min_score: number
}

export interface FailedTwiceResult {
  student_no: string
  name: string
  failed_count: number
}

export interface ClassAvgScore {
  class_no: string
  class_name: string
  avg_score: number
}

export interface TopSalaryResult {
  student_no: string
  name: string
  company: string
  salary: number
  position: string
}

export interface StudentOfferDuration {
  student_no: string
  name: string
  offer_duration_days: number
}

export interface ClassOfferDuration {
  class_no: string
  class_name: string
  avg_offer_duration_days: number
}

export interface ExamRankingItem {
  student_no: string
  student_name: string
  class_no: string
  class_name: string
  score: number
  rank: number
}

export interface ClassScoreReportItem {
  class_no: string
  class_name: string
  exam_no: number
  student_count: number
  avg_score: number
  excellent_rate: number
  pass_rate: number
  excellent_count: number
  pass_count: number
}
