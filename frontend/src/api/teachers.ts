import apiClient from './client'
import type { Teacher } from '@/types'

export const teacherApi = {
  getAll: () => apiClient.get<Teacher[]>('/teachers'),
  getById: (teacherNo: string) => apiClient.get<Teacher>(`/teachers/${teacherNo}`),
  create: (data: Omit<Teacher, 'teacher_no'> & { teacher_no: string }) => apiClient.post<Teacher>('/teachers', data),
  update: (teacherNo: string, data: Partial<Teacher>) => apiClient.put<Teacher>(`/teachers/${teacherNo}`, data),
  delete: (teacherNo: string) => apiClient.delete(`/teachers/${teacherNo}`),
}
