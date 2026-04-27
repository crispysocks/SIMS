export interface Student {
  student_no: string
  name: string
  class_no: string
  gender: string
  age?: number | null
  birth_place?: string | null
  graduate_school?: string | null
  major?: string | null
  entrance_time: string
  graduate_time?: string | null
  education: string
  advisor_name?: string | null
  phone?: string | null
  id_card?: string | null
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
  exam_name: string
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
  employment_status: number
  employment_open_time: string
  offer_time: string
  company: string
  salary: number
  position: string
  work_location: string
  is_deleted: boolean
}

export interface AvgSalaryByGroup {
  group_key: string
  avg_salary: number
  count: number
}

export interface ClassGenderStat {
  class_no: string
  class_name: string
  male_count: number
  female_count: number
  total: number
}

export interface ClassAvgScore {
  class_no: string
  class_name: string
  avg_score: number
}

export interface TopSalaryStudent {
  student_no: string
  name: string
  class_no: string
  salary: number
  company: string
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

export interface ProgressItem {
  student_no: string
  student_name: string
  class_no: string
  class_name: string
  previous_exam_no: number
  previous_exam_name: string
  previous_score: number
  latest_exam_no: number
  latest_exam_name: string
  latest_score: number
  score_diff: number
}

export interface ClassScoreReportItem {
  class_no: string
  class_name: string
  exam_no: number
  exam_name: string
  student_count: number
  avg_score: number
  excellent_rate: number
  pass_rate: number
  excellent_count: number
  pass_count: number
}
