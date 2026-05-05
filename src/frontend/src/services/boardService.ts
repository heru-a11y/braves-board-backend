// src/services/boardService.ts
// Semua API call yang berhubungan dengan Boards

import axios from 'axios'
import api from './api'

const BASE = 'http://localhost:8000'

// http — axios instance tanpa baseURL untuk endpoint non /api/v1
const http = axios.create({ baseURL: BASE })
http.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ─── Boards ───────────────────────────────────────────────────

export async function getBoards(limit = 100, offset = 0) {
  const res = await http.get('/boards', { params: { limit, offset } })
  return res.data?.data ?? res.data ?? {}
}

export async function createBoard(title: string) {
  const res = await http.post('/boards', { title })
  return res.data?.data ?? res.data
}

export async function getBoardDetail(boardId: string) {
  const res = await http.get(`/boards/${boardId}`)
  return res.data?.data ?? res.data
}

export async function updateBoard(boardId: string, title: string) {
  const res = await http.patch(`/boards/${boardId}`, { title })
  return res.data?.data ?? res.data
}

export async function deleteBoard(boardId: string) {
  await http.delete(`/boards/${boardId}`)
}

// ─── Users ───────────────────────────────────────────────────────

export async function getUsers() {
  const res = await http.get('/users')
  return res.data?.data ?? res.data ?? []
}

// ─── Comments ─────────────────────────────────────────────────

export async function addComment(taskId: string, content: string) {
  const res = await http.post(`/tasks/${taskId}/comments`, { content })
  return res.data?.data ?? res.data
}

export async function deleteComment(commentId: string) {
  await http.delete(`/tasks/comments/${commentId}`)
}

// ─── Attachments ──────────────────────────────────────────────

export async function uploadAttachmentFile(taskId: string, file: File) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await http.post(`/tasks/${taskId}/attachments/file`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data?.data ?? res.data
}

export async function addAttachmentLink(taskId: string, title: string, url: string) {
  const res = await http.post(`/tasks/${taskId}/attachments/link`, { title, url })
  return res.data?.data ?? res.data
}

export async function deleteAttachment(attachId: string) {
  await http.delete(`/tasks/attachments/${attachId}`)
}