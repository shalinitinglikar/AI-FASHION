import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { apiService } from '../services/api'
import OutfitCard from '../components/OutfitCard'

export default function DashboardPage() {
  const [outfits, setOutfits] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalOutfits: 0,
    favoriteStyles: [],
    recentRecommendations: 0
  })

  useEffect(() => {
    fetchOutfits()
  }, [])

  const fetchOutfits = async () => {
    try {
      const response = await apiService.getSavedOutfits()
      setOutfits(response.data)
      setStats({
        totalOutfits: response.data.length,
        favoriteStyles: ['Classic', 'Modern', 'Minimalist'],
        recentRecommendations: response.data.filter(o => o.created_at > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)).length
      })
    } catch (error) {
      console.error('Failed to fetch outfits:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteOutfit = async (outfitId) => {
    try {
      await apiService.deleteOutfit(outfitId)
      setOutfits(outfits.filter(o => o.id !== outfitId))
    } catch (error) {
      console.error('Failed to delete outfit:', error)
    }
  }

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg p-8"
      >
        <h1 className="text-4xl font-bold mb-2">Welcome to Your Fashion Dashboard</h1>
        <p className="text-lg opacity-90">Discover personalized outfit recommendations tailored to your style</p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-3 gap-6">
        {[
          { label: 'Total Outfits', value: stats.totalOutfits, icon: '👗' },
          { label: 'This Week', value: stats.recentRecommendations, icon: '✨' },
          { label: 'Favorite Styles', value: stats.favoriteStyles.length, icon: '🎨' }
        ].map((stat, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-white rounded-lg card-shadow p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">{stat.label}</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
              </div>
              <div className="text-4xl">{stat.icon}</div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg card-shadow p-8 text-center"
        >
          <h3 className="text-xl font-semibold mb-4">Get Recommendations</h3>
          <p className="text-gray-600 mb-6">Get AI-powered outfit suggestions based on your style</p>
          <button className="btn-primary">
            Explore Recommendations
          </button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg card-shadow p-8 text-center"
        >
          <h3 className="text-xl font-semibold mb-4">Style Analysis</h3>
          <p className="text-gray-600 mb-6">Upload an image for instant style analysis</p>
          <button className="btn-primary">
            Analyze Your Style
          </button>
        </motion.div>
      </div>

      {/* Recent Outfits */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Saved Outfits</h2>
        {loading ? (
          <p className="text-center text-gray-600">Loading outfits...</p>
        ) : outfits.length === 0 ? (
          <div className="bg-white rounded-lg card-shadow p-12 text-center">
            <p className="text-gray-600 mb-4">No saved outfits yet</p>
            <button className="btn-primary">
              Start Building Outfits
            </button>
          </div>
        ) : (
          <div className="grid md:grid-cols-4 gap-6">
            {outfits.map(outfit => (
              <OutfitCard
                key={outfit.id}
                outfit={outfit}
                onDelete={handleDeleteOutfit}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
