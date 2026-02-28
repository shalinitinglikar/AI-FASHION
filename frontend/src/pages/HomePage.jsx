import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function HomePage() {
  const { user } = useAuthStore()

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-white to-pink-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            AI Fashion
          </h1>
          <div className="space-x-4">
            {user ? (
              <Link to="/dashboard" className="btn-primary">
                Dashboard
              </Link>
            ) : (
              <>
                <Link to="/login" className="btn-secondary">
                  Login
                </Link>
                <Link to="/register" className="btn-primary">
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-20"
        >
          <h2 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Your Personal AI Fashion Stylist
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get personalized outfit recommendations, styling advice, and trend-aware suggestions powered by advanced AI analysis
          </p>
          <Link to={user ? '/dashboard' : '/register'} className="btn-primary text-lg">
            {user ? 'Go to Dashboard' : 'Start Your Journey'}
          </Link>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-20">
          {features.map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              className="bg-white rounded-lg card-shadow p-8 text-center hover:shadow-2xl transition"
            >
              <div className="text-5xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-3 text-gray-800">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg p-12 text-white text-center"
        >
          <h3 className="text-3xl font-bold mb-4">Ready to Transform Your Style?</h3>
          <p className="text-lg mb-8">Join thousands of users getting AI-powered fashion recommendations</p>
          <Link to={user ? '/dashboard' : '/register'} className="btn-primary bg-white text-purple-600 hover:text-pink-600">
            {user ? 'Go to Dashboard' : 'Create Your Account'}
          </Link>
        </motion.div>
      </section>
    </div>
  )
}

const features = [
  {
    icon: '👗',
    title: 'Smart Recommendations',
    description: 'Get personalized outfit suggestions based on your style, body type, and preferences'
  },
  {
    icon: '🎨',
    title: 'Color Analysis',
    description: 'Discover which colors complement your skin tone and personal style best'
  },
  {
    icon: '📸',
    title: 'Image Recognition',
    description: 'Upload photos and get instant analysis of clothing items and styling tips'
  },
  {
    icon: '🌍',
    title: 'Trend Insights',
    description: 'Stay updated with the latest fashion trends curated for your style'
  },
  {
    icon: '💾',
    title: 'Save Outfits',
    description: 'Build and organize your favorite outfit combinations for easy reference'
  },
  {
    icon: '✨',
    title: 'Styling Guidance',
    description: 'Get expert styling tips and guidance for different occasions and seasons'
  }
]
