import apiClient from './client'
import type { ClassInfo } from '@/types'

export const classApi = {
  getAll: () => apiClient.get<ClassInfo[]>('/classes'),
  getById: (classNo: string) => apiClient.get<ClassInfo>(`/classes/${classNo}`),
  create: (data: Omit<ClassInfo, 'class_no'> & { class_no: string }) => apiClient.post<ClassInfo>('/classes', data),
  update: (classNo: string, data: Partial<ClassInfo>) => apiClient.put<ClassInfo>(`/classes/${classNo}`, data),
  delete: (classNo: string) => apiClient.delete(`/classes/${classNo}`),
}
