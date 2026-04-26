import type { Teacher } from './teacher'

export interface ClassInfo {
  class_no: string
  class_name: string
  class_open_time: string
  head_teacher_no?: string
  instructor_no?: string
  description?: string
  isdeleted?: number
}

export interface ClassInfoCreate {
  class_no: string
  class_name: string
  class_open_time: string
  head_teacher_no?: string
  instructor_no?: string
  description?: string
}

export interface ClassInfoUpdate {
  class_name?: string
  class_open_time?: string
  head_teacher_no?: string
  instructor_no?: string
  description?: string
}

export interface ClassInfoDetail extends ClassInfo {
  headteacher?: Teacher
  instructor?: Teacher
}