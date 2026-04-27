import apiClient from './client'
import type { ClassScoreReportItem, ExamRankingItem, Score } from '@/types'

export const scoreApi = {
  getAll: () => apiClient.get<Score[]>('/scores/'),
  getByStudent: (studentNo: string) => apiClient.get<Score[]>(`/scores/${studentNo}`),
  create: (data: Omit<Score, 'student_no'> & { student_no: string }) => apiClient.post<Score>('/scores/', data),
  update: (data: Score) => apiClient.put<Score>('/scores/update', data),
  delete: (data: { student_no: string; exam_no: string }) => apiClient.post('/scores/delete', data),
  examRanking: (examNo: number) => apiClient.get<ExamRankingItem[]>(`/scores/ranking/exam?exam_no=${examNo}`),
  classScoreReport: (examNo: number) => apiClient.get<ClassScoreReportItem[]>(`/scores/report/class?exam_no=${examNo}`),
}
