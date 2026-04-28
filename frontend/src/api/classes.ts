import apiClient from './client'
import type { ClassInfo } from '@/types'

export interface ClassListResponse {
  classes: ClassInfo[]
  total: number
}

export interface ClassNamesResponse {
  names: string[]
}

export interface ClassCountResponse {
  total: number
}

export const classApi = {
  // 1. 分页+模糊查询班级列表（原 getAll 改为分页查询）
  getList: (skip: number, limit: number, className?: string) =>
    apiClient.get<ClassListResponse>(
      `/classes?skip=${skip}&limit=${limit}${className ? `&class_name=${encodeURIComponent(className)}` : ''}`
    ),

  // 2. 根据编号查询单个班级（原 getById，路径不变）
  getById: (classNo: string) => apiClient.get<ClassInfo>(`/classes/${classNo}`),

  // 3. 新增班级
  create: (data: Omit<ClassInfo, 'isdeleted'> & { class_no: string }) =>
    apiClient.post<ClassInfo>('/classes', data),

  // 4. 修改班级
  update: (classNo: string, data: Partial<ClassInfo>) =>
    apiClient.put<ClassInfo>(`/classes/${classNo}`, data),

  // 5. 删除班级
  delete: (classNo: string) => apiClient.delete(`/classes/${classNo}`),

  // 6. 获取所有班级名称（路径从 /names/all 改为 /names）
  getNames: () => apiClient.get<ClassNamesResponse>('/classes/names'),

  // 7. 统计班级总数（路径从 /count/total 改为 /count）
  getTotalCount: () => apiClient.get<ClassCountResponse>('/classes/count'),
}
