import apiClient from './client'
import type { EmploymentV2 } from '@/types'

export interface EmploymentQuery {
  student_no?: string
  company?: string
  position?: string
  work_location?: string
  min_salary?: number
  max_salary?: number
  employment_status?: number
}

export const employmentV2Api = {
  search: (query: EmploymentQuery) => apiClient.post<EmploymentV2[]>('/v2/employment/search', query),
  getById: (studentNo: string) => apiClient.get<EmploymentV2>(`/v2/employment/${studentNo}`),
  getByClass: (classNo: string) => apiClient.get<EmploymentV2[]>(`/v2/employment/class/${classNo}`),
  create: (data: Omit<EmploymentV2, 'is_deleted'>) => apiClient.post<EmploymentV2>('/v2/employment', data),
  update: (studentNo: string, data: Partial<EmploymentV2>) => apiClient.put<EmploymentV2>(`/v2/employment/${studentNo}`, data),
  batchDelete: (studentNos: string[]) => apiClient.delete('/v2/employment', { data: { student_nos: studentNos } }),
  batchRestore: (studentNos: string[]) => apiClient.put('/v2/employment/restore', { student_nos: studentNos }),
}
