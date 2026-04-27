import apiClient from './client'

export interface LoginParams {
  username: string
  password: string
}

export interface LoginResult {
  access_token: string
  token_type: string
  username: string
  roles: string[]
}

export async function login(data: LoginParams): Promise<LoginResult> {
  const res = await apiClient.post('/auth/login', data)
  return res.data
}

export async function register(data: LoginParams & { roles?: string }): Promise<LoginResult> {
  const res = await apiClient.post('/auth/register', data)
  return res.data
}
