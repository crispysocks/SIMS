import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/Index.vue')
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/Index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/students',
    name: 'Students',
    component: () => import('@/views/student/Index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/students/form',
    name: 'StudentForm',
    component: () => import('@/views/student/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/students/form/:studentNo',
    name: 'StudentEdit',
    component: () => import('@/views/student/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/students/:studentNo',
    name: 'StudentDetail',
    component: () => import('@/views/student/Detail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component: () => import('@/views/teacher/Index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/teachers/form',
    name: 'TeacherForm',
    component: () => import('@/views/teacher/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/teachers/form/:teacherNo',
    name: 'TeacherEdit',
    component: () => import('@/views/teacher/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/classes',
    name: 'Classes',
    component: () => import('@/views/classes/Index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/classes/form',
    name: 'ClassForm',
    component: () => import('@/views/classes/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/classes/form/:classNo',
    name: 'ClassEdit',
    component: () => import('@/views/classes/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/scores',
    name: 'Scores',
    component: () => import('@/views/score/Index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/scores/form',
    name: 'ScoreForm',
    component: () => import('@/views/score/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/employment',
    name: 'Employment',
    component: () => import('@/views/employment/Index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/employment/:studentNo',
    name: 'EmploymentDetail',
    component: () => import('@/views/employment/Detail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/employment/form',
    name: 'EmploymentForm',
    component: () => import('@/views/employment/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/employment/form/:studentNo',
    name: 'EmploymentEdit',
    component: () => import('@/views/employment/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('@/views/statistics/Index.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.path === '/login') {
    if (authStore.isLoggedIn) {
      next('/')
    } else {
      next()
    }
  } else if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router