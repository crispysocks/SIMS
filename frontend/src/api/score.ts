import { get, post, put, del } from '@/api/request'
import type { Score, ScoreCreate, ScoreUpdate } from '@/types/score'

export const getScores = (studentNo: string) =>
  get<Score[]>(`/scores/${studentNo}`)

export const createScore = (data: ScoreCreate) =>
  post<Score>('/scores/', data)

export const updateScore = (data: ScoreUpdate) =>
  put<Score>('/scores/update', data)

export const deleteScore = (data: { student_no: string; exam_no: number; exam_name: string }) =>
  del<{ message: string }>('/scores/delete', data)