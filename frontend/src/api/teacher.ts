import { get, post, put, del } from '@/api/request'
import type { Teacher, TeacherCreate, TeacherUpdate } from '@/types/teacher'

export const getTeachers = (params?: Record<string, unknown>) =>
  get<Teacher[]>('/teachers', params)

export const getTeacher = (teacherNo: string) =>
  get<Teacher>(`/teachers/${teacherNo}`)

export const createTeacher = (data: TeacherCreate) =>
  post<Teacher>('/teachers', data)

export const updateTeacher = (teacherNo: string, data: TeacherUpdate) =>
  put<Teacher>(`/teachers/${teacherNo}`, data)

export const deleteTeacher = (teacherNo: string) =>
  del<{ message: string }>(`/teachers/${teacherNo}`)