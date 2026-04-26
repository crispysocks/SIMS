import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const username = ref<string>('')
  const roles = ref<string[]>([])

  const isLoggedIn = computed(() => !!username.value)
  const isAdmin = computed(() => roles.value.includes('admin'))
  const isTeacher = computed(() => roles.value.includes('teacher'))

  function hasRole(role: string) {
    return roles.value.includes(role)
  }

  function login(name: string, userRoles: string[]) {
    username.value = name
    roles.value = userRoles
  }

  function logout() {
    username.value = ''
    roles.value = []
  }

  return {
    username,
    roles,
    isLoggedIn,
    isAdmin,
    isTeacher,
    hasRole,
    login,
    logout
  }
})