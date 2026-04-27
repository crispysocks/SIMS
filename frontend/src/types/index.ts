export interface Student {
  student_no: string
  name: string
  class_no: string
  gender: string
  age: number
  native_place: string
  graduation_school: string
  major: string
  enrollment_time: string
  graduation_time: string
  education_level: string
  consultant: string
  phone: string
  id_card: string
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
  remark: string
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
