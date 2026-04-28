import apiClient from './client'
import type { Student, ClassGenderStat, ClassAvgScore, TopSalaryStudent, StudentOfferDuration, ClassOfferDuration } from '@/types'

export const statisticsApi = {
  ageFilter: (age: number) => apiClient.get<Student[]>(`/statistics/age-filter?age=${age}`),
  classGender: () => apiClient.get<ClassGenderStat[]>('/statistics/class-gender'),
  alwaysAbove: (score: number) => apiClient.get<Student[]>(`/statistics/always-above?score=${score}`),
  failedTwice: () => apiClient.get<Student[]>('/statistics/failed-twice'),
  classAvgScore: () => apiClient.get<ClassAvgScore[]>('/statistics/class-avg-score'),
  topSalary: () => apiClient.get<TopSalaryStudent[]>('/statistics/top-salary'),
  studentOfferDuration: () => apiClient.get<StudentOfferDuration[]>('/statistics/student-offer-duration'),
  classOfferDuration: () => apiClient.get<ClassOfferDuration[]>('/statistics/class-offer-duration'),
}
