import apiClient from './client'

export interface User {
  id: number
  username: string
  roles: string
  is_active: number
  created_at: string
}

export interface UserUpdateParams {
  roles?: string
  is_active?: number
  password?: string
}

export async function getUsers(): Promise<User[]> {
  const res = await apiClient.get('/users')
  return res.data
}

export async function updateUser(id: number, data: UserUpdateParams): Promise<User> {
  const res = await apiClient.put(`/users/${id}`, data)
  return res.data
}

export async function deleteUser(id: number): Promise<void> {
  await apiClient.delete(`/users/${id}`)
}
