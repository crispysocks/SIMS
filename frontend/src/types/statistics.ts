export interface StudentAgeFilter {
  student_no: string
  name: string
  age: number
}

export interface ClassGenderStat {
  class_no: string
  class_name: string
  male_count: number
  female_count: number
}

export interface ScoreAlwaysAbove {
  student_no: string
  name: string
  exam_name: string
  min_score: number
}

export interface FailedTwice {
  student_no: string
  name: string
  class_no: string
  fail_count: number
}

export interface ClassAvgScore {
  class_no: string
  class_name: string
  avg_score: number
}

export interface TopSalary {
  student_no: string
  name: string
  class_no: string
  company: string
  salary: number
}

export interface StudentOfferDuration {
  student_no: string
  name: string
  duration_days: number
}

export interface ClassOfferDuration {
  class_no: string
  class_name: string
  avg_duration_days: number
}