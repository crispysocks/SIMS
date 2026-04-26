import { ElMessage } from 'element-plus'
import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'
import type { ApiResponse } from '@/types/api'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const request: AxiosInstance = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const authStore = useAuthStore()
    if (authStore.username) {
      config.headers.set('X-User', authStore.username)
    }
    if (authStore.roles.length > 0) {
      config.headers.set('X-Roles', authStore.roles.join(','))
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  (response: AxiosResponse<ApiResponse<unknown>>) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      router.push('/login')
    } else if (error.response?.status === 403) {
      ElMessage.error('没有访问权限')
    } else if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else if (error.message) {
      ElMessage.error(error.message)
    }
    return Promise.reject(error)
  }
)

export default request

export const get = <T>(url: string, params?: Record<string, unknown>) =>
  request.get<ApiResponse<T>>(url, { params }).then(res => res.data)

export const post = <T>(url: string, data?: Record<string, unknown>) =>
  request.post<ApiResponse<T>>(url, data).then(res => res.data)

export const put = <T>(url: string, data?: Record<string, unknown>) =>
  request.put<ApiResponse<T>>(url, data).then(res => res.data)

export const del = <T>(url: string, data?: Record<string, unknown>) =>
  request.delete<ApiResponse<T>>(url, { data }).then(res => res.data)