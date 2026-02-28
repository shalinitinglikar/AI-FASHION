import { useAuthStore } from '../store/authStore'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Layout({ children }) {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 to-pink-100">
      {/* Navigation */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/dashboard" className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              AI Fashion
            </Link>

            <div className="flex items-center space-x-8">
              <Link to="/recommendations" className="text-gray-600 hover:text-purple-600 transition">
                Recommendations
              </Link>
              <Link to="/style-analysis" className="text-gray-600 hover:text-purple-600 transition">
                Style Analysis
              </Link>
              <Link to="/profile" className="text-gray-600 hover:text-purple-600 transition">
                Profile
              </Link>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">{user?.username}</span>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:shadow-lg transition"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {children}
        </motion.div>
      </main>
    </div>
  )
}
