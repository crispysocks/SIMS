import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

apiClient.interceptors.request.use((config) => {
  const { token } = useAuthStore.getState()
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => {
    const data = response.data
    if (data && typeof data === 'object' && 'data' in data) {
      response.data = data.data
    }
    return response
  },
  (error) => {
    const status = error.response?.status
    const data = error.response?.data
    let msg: string
    if (Array.isArray(data?.detail)) {
      msg = data.detail.map((d: any) => d.msg || JSON.stringify(d)).join('; ')
    } else {
      msg = data?.detail || error.message || '请求失败'
    }
    if (status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    console.error('[API Error]', status, data)
    return Promise.reject(new Error(msg))
  }
)

export default apiClient
