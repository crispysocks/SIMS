import { get, post, put, del } from '@/api/request'
import type { Student, StudentCreate, StudentUpdate } from '@/types'
import type { ApiResponse, PaginatedResponse } from '@/types/api'

export const getStudents = (params?: Record<string, unknown>) =>
  get<PaginatedResponse<Student>>('/students/all', params)

export const searchStudents = (name: string) =>
  get<Student[]>('/students/search', { name })

export const getStudent = (studentNo: string) =>
  get<Student>(`/students/${studentNo}`)

export const getStudentsByClass = (classNo: string) =>
  get<Student[]>(`/students/class/${classNo}`)

export const createStudent = (data: StudentCreate) =>
  post<Student>('/students/add', data)

export const updateStudent = (studentNo: string, data: StudentUpdate) =>
  put<Student>(`/students/${studentNo}`, data)

export const deleteStudents = (studentNos: string[]) =>
  del<{ message: string }>('/students/batch', { student_nos: studentNos })

export const restoreStudents = (studentNos: string[]) =>
  del<{ message: string }>('/students/back', { student_nos: studentNos })