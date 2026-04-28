import apiClient from './client'
import type { Teacher, TeacherGenderStat } from '@/types'

export const teacherApi = {
  getAll: () => apiClient.get<Teacher[]>('/teachers'),
  getById: (teacherNo: string) => apiClient.get<Teacher>(`/teachers/${teacherNo}`),
  create: (data: Omit<Teacher, 'teacher_no'> & { teacher_no: string }) => apiClient.post<Teacher>('/teachers', data),
  update: (teacherNo: string, data: Partial<Teacher>) => apiClient.put<Teacher>(`/teachers/${teacherNo}`, data),
  delete: (teacherNos: string[]) => apiClient.delete('/teachers', { data: teacherNos }),
  search: (params: { name?: string; gender?: string }) =>
    apiClient.get<Teacher[]>('/teachers/search/by-name-or-gender', { params }),
  genderStats: () => apiClient.get<TeacherGenderStat[]>('/teachers/stats/gender'),
}
