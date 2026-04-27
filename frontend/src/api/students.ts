import apiClient from './client'
import type { Student } from '@/types'

export const studentApi = {
  getAll: () => apiClient.get<Student[]>('/students/all'),
  search: (name: string) => apiClient.get<Student[]>(`/students/search?name=${encodeURIComponent(name)}`),
  getByClass: (classNo: string) => apiClient.get<Student[]>(`/students/class/${classNo}`),
  getById: (studentNo: string) => apiClient.get<Student>(`/students/${studentNo}`),
  create: (data: Omit<Student, 'student_no'> & { student_no: string }) => apiClient.post<Student>('/students/add', data),
  update: (studentNo: string, data: Partial<Student>) => apiClient.put<Student>(`/students/${studentNo}`, data),
  batchDelete: (noList: string[]) => apiClient.delete('/students/batch', { data: { no_list: noList } }),
  batchRestore: (noList: string[]) => apiClient.delete('/students/back', { data: { no_list: noList } }),
}
