import { get } from '@/api/request'
import type {
  StudentAgeFilter,
  ClassGenderStat,
  ScoreAlwaysAbove,
  FailedTwice,
  ClassAvgScore,
  TopSalary,
  StudentOfferDuration,
  ClassOfferDuration
} from '@/types/statistics'

export const getAgeFilter = (age: number) =>
  get<StudentAgeFilter[]>('/api/statistics/age-filter', { age })

export const getClassGender = () =>
  get<ClassGenderStat[]>('/api/statistics/class-gender')

export const getScoreAlwaysAbove = (score: number) =>
  get<ScoreAlwaysAbove[]>('/api/statistics/always-above', { score })

export const getFailedTwice = () =>
  get<FailedTwice[]>('/api/statistics/failed-twice')

export const getClassAvgScore = () =>
  get<ClassAvgScore[]>('/api/statistics/class-avg-score')

export const getTopSalary = (limit?: number) =>
  get<TopSalary[]>('/api/statistics/top-salary', { limit })

export const getStudentOfferDuration = (studentNo: string) =>
  get<StudentOfferDuration>('/api/statistics/student-offer-duration', { student_no: studentNo })

export const getClassOfferDuration = () =>
  get<ClassOfferDuration[]>('/api/statistics/class-offer-duration')