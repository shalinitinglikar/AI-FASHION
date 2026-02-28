import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { apiService } from '../services/api'
import OutfitCard from '../components/OutfitCard'

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const [occasion, setOccasion] = useState('casual')
  const [season, setSeason] = useState('spring')

  useEffect(() => {
    fetchRecommendations()
  }, [occasion, season])

  const fetchRecommendations = async () => {
    setLoading(true)
    try {
      const response = await apiService.getRecommendations({ occasion, season })
      setRecommendations(response.data)
    } catch (error) {
      console.error('Failed to fetch recommendations:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveOutfit = async (outfit) => {
    try {
      await apiService.saveOutfit(outfit)
      alert('Outfit saved successfully!')
    } catch (error) {
      console.error('Failed to save outfit:', error)
    }
  }

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg p-8"
      >
        <h1 className="text-4xl font-bold mb-2">Outfit Recommendations</h1>
        <p className="text-lg opacity-90">Personalized suggestions for every occasion</p>
      </motion.div>

      {/* Filters */}
      <div className="bg-white rounded-lg card-shadow p-6">
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Occasion</label>
            <select
              value={occasion}
              onChange={(e) => setOccasion(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            >
              <option value="casual">Casual</option>
              <option value="formal">Formal</option>
              <option value="business">Business</option>
              <option value="party">Party</option>
              <option value="gym">Gym</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Season</label>
            <select
              value={season}
              onChange={(e) => setSeason(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            >
              <option value="spring">Spring</option>
              <option value="summer">Summer</option>
              <option value="fall">Fall</option>
              <option value="winter">Winter</option>
            </select>
          </div>
        </div>
      </div>

      {/* Recommendations Grid */}
      {loading ? (
        <div className="text-center py-12">
          <p className="text-gray-600">Loading recommendations...</p>
        </div>
      ) : recommendations.length === 0 ? (
        <div className="bg-white rounded-lg card-shadow p-12 text-center">
          <p className="text-gray-600">No recommendations available for these filters</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-4 gap-6">
          {recommendations.map(outfit => (
            <OutfitCard
              key={outfit.id}
              outfit={outfit}
              onSave={handleSaveOutfit}
            />
          ))}
        </div>
      )}
    </div>
  )
}
