import apiClient from './client'
import type { Student, ClassGenderStat, ClassAvgScore, TopSalaryStudent, StudentOfferDuration, ClassOfferDuration } from '@/types'

export const statisticsApi = {
  ageFilter: (age: number) => apiClient.get<Student[]>(`/api/statistics/age-filter?age=${age}`),
  classGender: () => apiClient.get<ClassGenderStat[]>('/api/statistics/class-gender'),
  alwaysAbove: (score: number) => apiClient.get<Student[]>(`/api/statistics/always-above?score=${score}`),
  failedTwice: () => apiClient.get<Student[]>('/api/statistics/failed-twice'),
  classAvgScore: () => apiClient.get<ClassAvgScore[]>('/api/statistics/class-avg-score'),
  topSalary: () => apiClient.get<TopSalaryStudent[]>('/api/statistics/top-salary'),
  studentOfferDuration: () => apiClient.get<StudentOfferDuration[]>('/api/statistics/student-offer-duration'),
  classOfferDuration: () => apiClient.get<ClassOfferDuration[]>('/api/statistics/class-offer-duration'),
}
