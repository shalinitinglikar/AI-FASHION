import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

const getAuthHeader = () => {
  const token = localStorage.getItem('token')
  return {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  }
}

export const apiService = {
  // Recommendations
  getRecommendations: (params) =>
    axios.get(`${API_URL}/recommendations`, { ...getAuthHeader(), params }),

  generateRecommendations: (preferencesId) =>
    axios.post(`${API_URL}/recommendations/generate`, { preferencesId }, getAuthHeader()),

  // Image Analysis
  analyzeImage: (formData) =>
    axios.post(`${API_URL}/images/analyze`, formData, {
      ...getAuthHeader(),
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }),

  uploadStyleImage: (formData) =>
    axios.post(`${API_URL}/images/upload-style`, formData, {
      ...getAuthHeader(),
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }),

  // User Profile
  getUserProfile: () =>
    axios.get(`${API_URL}/users/profile`, getAuthHeader()),

  updateUserProfile: (data) =>
    axios.put(`${API_URL}/users/profile`, data, getAuthHeader()),

  updateStylePreferences: (preferences) =>
    axios.put(`${API_URL}/users/preferences`, preferences, getAuthHeader()),

  // Saved Outfits
  getSavedOutfits: () =>
    axios.get(`${API_URL}/users/outfits`, getAuthHeader()),

  saveOutfit: (outfitData) =>
    axios.post(`${API_URL}/users/outfits`, outfitData, getAuthHeader()),

  deleteOutfit: (outfitId) =>
    axios.delete(`${API_URL}/users/outfits/${outfitId}`, getAuthHeader())
}
