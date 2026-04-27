import apiClient from './client'
import type { Score } from '@/types'

export const scoreApi = {
  getByStudent: (studentNo: string) => apiClient.get<Score[]>(`/scores/${studentNo}`),
  create: (data: Omit<Score, 'student_no'> & { student_no: string }) => apiClient.post<Score>('/scores/', data),
  update: (data: Score) => apiClient.put<Score>('/scores/update', data),
  delete: (data: { student_no: string; exam_no: string; exam_name: string }) => apiClient.post('/scores/delete', data),
}
