// src/services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
})

// 🔥 AUTO INJECT TOKEN
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})


// Response interceptor: auto-refresh jika 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const { data } = await api.post('/auth/refresh')
        const newToken = data.data?.access_token || data.access_token

        if (newToken) {
          localStorage.setItem('access_token', newToken)
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return api(originalRequest)
        }
      } catch {
        // Refresh gagal → hapus token & redirect ke login
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        window.location.href = '/'
      }
    }

    return Promise.reject(error)
  },
)

export default api
