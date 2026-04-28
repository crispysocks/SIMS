import apiClient from './client'
import type { Employment, AvgSalaryByGroup } from '@/types'

export const employmentApi = {
  getByStudent: (studentNo: string) => apiClient.get<Employment>(`/employment/students/${studentNo}`),
  getByClass: (classNo: string) => apiClient.get<Employment[]>(`/employment/class/${classNo}`),
  getBySalary: (minSalary: number) => apiClient.get<Employment[]>(`/employment/salary?min_salary=${minSalary}`),
  getByStatus: (status: number) => apiClient.get<Employment[]>(`/employment/status/${status}`),
  getAvgSalary: (groupBy: 'class' | 'gender') => apiClient.get<AvgSalaryByGroup[]>(`/employment/avg-salary?group_by=${groupBy}`),
  create: (studentNo: string, data: Omit<Employment, 'student_no'>) => apiClient.post<Employment>(`/employment/students/${studentNo}`, data),
  update: (studentNo: string, data: Partial<Employment>) => apiClient.put<Employment>(`/employment/students/${studentNo}`, data),
  delete: (studentNo: string) => apiClient.delete(`/employment/students/${studentNo}`),
}
