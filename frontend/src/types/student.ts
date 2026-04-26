export type Gender = '男' | '女'
export type Education = '专科' | '本科' | '硕士'

export interface Student {
  student_no: string
  class_no: string
  name: string
  birth_place?: string
  graduate_school?: string
  major?: string
  entrance_time: string
  graduate_time?: string
  education?: Education
  advisor_name?: string
  age?: number
  gender: Gender
  phone?: string
  id_card?: string
  isdeleted?: number
}

export interface StudentCreate {
  student_no: string
  class_no: string
  name: string
  birth_place?: string
  graduate_school?: string
  major?: string
  entrance_time: string
  graduate_time?: string
  education?: Education
  advisor_name?: string
  age?: number
  gender: Gender
  phone?: string
  id_card?: string
}

export interface StudentUpdate {
  class_no?: string
  name?: string
  birth_place?: string
  graduate_school?: string
  major?: string
  entrance_time?: string
  graduate_time?: string
  education?: Education
  advisor_name?: string
  age?: number
  gender?: Gender
  phone?: string
  id_card?: string
}