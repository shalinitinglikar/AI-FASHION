import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import RecommendationsPage from './pages/RecommendationsPage'
import StyleAnalysisPage from './pages/StyleAnalysisPage'
import ProfilePage from './pages/ProfilePage'

export default function App() {
  const { user } = useAuthStore()

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <LoginPage />} />
        <Route path="/register" element={user ? <Navigate to="/dashboard" /> : <RegisterPage />} />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={user ? <Layout><DashboardPage /></Layout> : <Navigate to="/login" />}
        />
        <Route
          path="/recommendations"
          element={user ? <Layout><RecommendationsPage /></Layout> : <Navigate to="/login" />}
        />
        <Route
          path="/style-analysis"
          element={user ? <Layout><StyleAnalysisPage /></Layout> : <Navigate to="/login" />}
        />
        <Route
          path="/profile"
          element={user ? <Layout><ProfilePage /></Layout> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  )
}
