import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { apiService } from '../services/api'
import { useAuthStore } from '../store/authStore'

export default function ProfilePage() {
  const { user } = useAuthStore()
  const [profile, setProfile] = useState(null)
  const [editing, setEditing] = useState(false)
  const [loading, setLoading] = useState(true)
  const [formData, setFormData] = useState({})

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const response = await apiService.getUserProfile()
      setProfile(response.data)
      setFormData(response.data)
    } catch (error) {
      console.error('Failed to fetch profile:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSave = async () => {
    try {
      await apiService.updateUserProfile(formData)
      setProfile(formData)
      setEditing(false)
      alert('Profile updated successfully!')
    } catch (error) {
      console.error('Failed to update profile:', error)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading profile...</div>
  }

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg p-8"
      >
        <h1 className="text-4xl font-bold mb-2">My Profile</h1>
        <p className="text-lg opacity-90">Manage your style preferences and account settings</p>
      </motion.div>

      <div className="bg-white rounded-lg card-shadow p-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Profile Information</h2>
          <button
            onClick={() => setEditing(!editing)}
            className="btn-primary"
          >
            {editing ? 'Cancel' : 'Edit'}
          </button>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
            <input
              type="text"
              name="first_name"
              value={formData.first_name || ''}
              onChange={handleChange}
              disabled={!editing}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg disabled:bg-gray-100 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
            <input
              type="text"
              name="last_name"
              value={formData.last_name || ''}
              onChange={handleChange}
              disabled={!editing}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg disabled:bg-gray-100 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email || ''}
              disabled
              className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
            <input
              type="text"
              name="username"
              value={formData.username || ''}
              disabled
              className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Body Type</label>
            <select
              name="body_type"
              value={formData.body_type || ''}
              onChange={handleChange}
              disabled={!editing}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg disabled:bg-gray-100 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            >
              <option value="">Select body type</option>
              <option value="Pear">Pear</option>
              <option value="Apple">Apple</option>
              <option value="Hourglass">Hourglass</option>
              <option value="Rectangle">Rectangle</option>
              <option value="Inverted Triangle">Inverted Triangle</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Climate Preference</label>
            <select
              name="climate_preference"
              value={formData.climate_preference || ''}
              onChange={handleChange}
              disabled={!editing}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg disabled:bg-gray-100 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            >
              <option value="">Select climate</option>
              <option value="Tropical">Tropical</option>
              <option value="Temperate">Temperate</option>
              <option value="Cold">Cold</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Budget Range</label>
            <input
              type="text"
              name="budget_range"
              value={formData.budget_range || ''}
              onChange={handleChange}
              disabled={!editing}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg disabled:bg-gray-100 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
              placeholder="e.g., $100-$500"
            />
          </div>
        </div>

        {editing && (
          <button
            onClick={handleSave}
            className="mt-6 btn-primary"
          >
            Save Changes
          </button>
        )}
      </div>
    </div>
  )
}
