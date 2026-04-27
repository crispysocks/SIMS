import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { Layout } from '@/components/layout/Layout'
import LoginPage from '@/pages/Login'
import DashboardPage from '@/pages/Dashboard'
import StudentsPage from '@/pages/Students'

import TeachersPage from '@/pages/Teachers'
import ClassesPage from '@/pages/Classes'
import ScoresPage from '@/pages/Scores'
import EmploymentPage from '@/pages/Employment'
import EmploymentV2Page from '@/pages/EmploymentV2'
import StatisticsPage from '@/pages/Statistics'
import UsersPage from '@/pages/Users'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isLoggedIn } = useAuthStore()
  return isLoggedIn ? <>{children}</> : <Navigate to="/login" replace />
}

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="students" element={<StudentsPage />} />

        <Route path="teachers" element={<TeachersPage />} />
        <Route path="classes" element={<ClassesPage />} />
        <Route path="scores" element={<ScoresPage />} />
        <Route path="employment" element={<EmploymentPage />} />
        <Route path="employment-v2" element={<EmploymentV2Page />} />
        <Route path="statistics" element={<StatisticsPage />} />
        <Route path="users" element={<UsersPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
