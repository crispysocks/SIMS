import { get, post, put, del } from '@/api/request'
import type { ClassInfo, ClassInfoCreate, ClassInfoUpdate, ClassInfoDetail } from '@/types/classes'

export const getClasses = (params?: Record<string, unknown>) =>
  get<ClassInfo[]>('/classes', params)

export const getClass = (classNo: string) =>
  get<ClassInfoDetail>(`/classes/${classNo}`)

export const createClass = (data: ClassInfoCreate) =>
  post<ClassInfo>('/classes', data)

export const updateClass = (classNo: string, data: ClassInfoUpdate) =>
  put<ClassInfo>(`/classes/${classNo}`, data)

export const deleteClass = (classNo: string) =>
  del<{ message: string }>(`/classes/${classNo}`)