import { get, post, put, del } from '@/api/request'
import type { Employment, EmploymentCreate, EmploymentUpdate, EmploymentSearch, EmploymentSearchResult } from '@/types/employment'

export const getEmployment = (studentNo: string) =>
  get<Employment>(`/employment/students/${studentNo}`)

export const getEmploymentsByClass = (classNo: string) =>
  get<Employment[]>(`/employment/class/${classNo}`)

export const createEmployment = (studentNo: string, data: Partial<Employment>) =>
  post<Employment>(`/employment/students/${studentNo}`, data)

export const updateEmployment = (studentNo: string, data: EmploymentUpdate) =>
  put<Employment>(`/employment/students/${studentNo}`, data)

export const deleteEmployment = (studentNo: string) =>
  del<{ message: string }>(`/employment/students/${studentNo}`)

export const getSalaryEmployments = (minSalary?: number) =>
  get<Employment[]>('/employment/salary', { min_salary: minSalary })

export const getAvgSalary = (groupBy?: string) =>
  get<{ class_no: string; avg_salary: number }[]>('/employment/avg-salary', { group_by: groupBy })

export const getEmploymentsByStatus = (status: string) =>
  get<Employment[]>(`/employment/status/${status}`)

export const v2GetEmployment = (studentNo: string) =>
  get<Employment>(`/v2/employment/${studentNo}`)

export const v2GetEmploymentsByClass = (classNo: string) =>
  get<Employment[]>(`/v2/employment/class/${classNo}`)

export const v2CreateEmployment = (data: EmploymentCreate) =>
  post<Employment>('/v2/employment', data)

export const v2UpdateEmployment = (studentNo: string, data: EmploymentUpdate) =>
  put<Employment>(`/v2/employment/${studentNo}`, data)

export const v2DeleteEmployments = (studentNos: string[]) =>
  del<{ message: string }>('/v2/employment', { student_nos: studentNos })

export const v2RestoreEmployments = (studentNos: string[]) =>
  put<{ message: string }>('/v2/employment/restore', { student_nos: studentNos })

export const v2SearchEmployments = (data: EmploymentSearch) =>
  post<EmploymentSearchResult[]>('/v2/employment/search', data)