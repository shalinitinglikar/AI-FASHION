import { create } from 'zustand'
import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

export const useAuthStore = create((set) => ({
  user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
  token: localStorage.getItem('token'),
  loading: false,
  error: null,

  register: async (email, username, password, userData) => {
    set({ loading: true, error: null })
    try {
      const response = await axios.post(`${API_URL}/auth/register`, {
        email,
        username,
        password,
        ...userData
      })
      const { user, token } = response.data
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('token', token)
      set({ user, token, loading: false })
      return response.data
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Registration failed'
      set({ error: errorMsg, loading: false })
      throw error
    }
  },

  login: async (email, password) => {
    set({ loading: true, error: null })
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        email,
        password
      })
      const { user, token } = response.data
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('token', token)
      set({ user, token, loading: false })
      return response.data
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Login failed'
      set({ error: errorMsg, loading: false })
      throw error
    }
  },

  logout: () => {
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    set({ user: null, token: null })
  }
}))
