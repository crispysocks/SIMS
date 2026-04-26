export type Gender = '男' | '女'

export interface Teacher {
  teacher_no: string
  name: string
  gender: Gender
  phone?: string
  email?: string
  id_card?: string
  birthday?: string
  hire_date?: string
  subject?: string
  isdeleted?: number
}

export interface TeacherCreate {
  teacher_no: string
  name: string
  gender: Gender
  phone?: string
  email?: string
  id_card?: string
  birthday?: string
  hire_date?: string
  subject?: string
}

export interface TeacherUpdate {
  name?: string
  gender?: Gender
  phone?: string
  email?: string
  id_card?: string
  birthday?: string
  hire_date?: string
  subject?: string
}