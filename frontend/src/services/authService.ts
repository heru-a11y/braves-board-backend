// src/services/authService.ts
import api from './api'
import axios from 'axios'


const BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:8000/api/v1'

export interface User {
  id: string
  email: string
  full_name: string
  picture_url?: string
}

export interface AuthTokens {
  access_token: string
}

// 🔥 1. Ambil URL login Google dari backend
export async function getGoogleLoginUrl(): Promise<string> {
  const { data } = await axios.get(`${BASE_URL}/auth/google/login`)

  const url =
    data?.data?.auth_url ||
    data?.auth_url ||
    data?.url

  if (!url) {
    throw new Error('URL Google OAuth tidak ditemukan')
  }

  return url
}

// 🔥 2. Simpan token dari URL (dipanggil di Dashboard)
export function saveTokenFromUrl() {
  const params = new URLSearchParams(window.location.search)
  const token = params.get('access_token')

  if (token) {
    localStorage.setItem('access_token', token)

    // bersihin URL
    window.history.replaceState({}, document.title, '/dashboard')
  }

  return token
}

// 🔥 3. Ambil user yang sedang login
export async function getCurrentUser(): Promise<User> {
  const res = await api.get('/auth/me')

  const user = res.data?.data

  if (!user) {
    throw new Error('User tidak ditemukan')
  }

  localStorage.setItem('user', JSON.stringify(user))

  return user
}

// 🔥 4. Refresh token (pakai cookie dari backend)
export async function refreshToken(): Promise<AuthTokens> {
  const { data } = await api.post('/auth/refresh')

  const token =
    data?.data?.access_token ||
    data?.access_token

  if (token) {
    localStorage.setItem('access_token', token)
  }

  return { access_token: token }
}

// 🔥 5. Logout
export async function logout() {
  try {
    await api.post('/auth/logout')
  } catch (err) {
    console.warn('Logout error:', err)
  }

  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
}