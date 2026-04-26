export interface Employment {
  student_no: string
  open_time?: string
  offer_time?: string
  company?: string
  salary?: number
  status?: string
  isdeleted?: number
}

export interface EmploymentCreate {
  student_no: string
  open_time: string
  offer_time: string
  company: string
  salary: number
}

export interface EmploymentUpdate {
  open_time?: string
  offer_time?: string
  company?: string
  salary?: number
  status?: string
}

export interface EmploymentSearch {
  student_no?: string
  company?: string
  min_salary?: number
  max_salary?: number
}

export interface EmploymentSearchResult {
  student_no: string
  student_name: string
  class_no: string
  company: string
  salary: number
  open_time?: string
  offer_time?: string
}