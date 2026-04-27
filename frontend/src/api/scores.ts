import apiClient from './client'
import type { ClassScoreReportItem, ExamRankingItem, ProgressItem, Score } from '@/types'

export const scoreApi = {
  getByStudent: (studentNo: string) => apiClient.get<Score[]>(`/scores/${studentNo}`),
  create: (data: Omit<Score, 'student_no'> & { student_no: string }) => apiClient.post<Score>('/scores/', data),
  update: (data: Score) => apiClient.put<Score>('/scores/update', data),
  delete: (data: { student_no: string; exam_no: string; exam_name: string }) => apiClient.post('/scores/delete', data),
  examRanking: (examNo: number, examName: string) => apiClient.get<ExamRankingItem[]>(`/scores/ranking/exam?exam_no=${examNo}&exam_name=${encodeURIComponent(examName)}`),
  progressRanking: (limit = 20) => apiClient.get<ProgressItem[]>(`/scores/ranking/progress?limit=${limit}`),
  classScoreReport: (examNo: number, examName: string) => apiClient.get<ClassScoreReportItem[]>(`/scores/report/class?exam_no=${examNo}&exam_name=${encodeURIComponent(examName)}`),
}
