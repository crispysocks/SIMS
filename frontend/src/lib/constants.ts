export const ROLES = {
  ADMIN: 'admin',
  TEACHER: 'teacher',
} as const

export const PERMISSIONS = {
  canEditScore: (roles: string[]) => roles.includes(ROLES.ADMIN) || roles.includes(ROLES.TEACHER),
  canDeleteScore: (roles: string[]) => roles.includes(ROLES.ADMIN),
  canEditEmployment: (roles: string[]) => roles.includes(ROLES.ADMIN) || roles.includes(ROLES.TEACHER),
  canDeleteEmployment: (roles: string[]) => roles.includes(ROLES.ADMIN),
  canManageStudent: (roles: string[]) => roles.includes(ROLES.ADMIN),
} as const

export const GENDER_MAP: Record<string, string> = {
  '男': '男',
  '女': '女',
  'male': '男',
  'female': '女',
  'other': '其他',
}

export const EMPLOYMENT_STATUS_MAP: Record<number, string> = {
  0: '已删除',
  1: '正常',
}
