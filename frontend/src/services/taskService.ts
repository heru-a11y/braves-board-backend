import axios from 'axios'

const http = axios.create({ baseURL: 'http://localhost:8000' })
http.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export async function getTasks(columnId: string) {
  const res = await http.get('/tasks', { params: { column_id: columnId } })
  return res.data?.data ?? res.data ?? []
}

export async function getTaskDetail(taskId: string) {
  const res = await http.get(`/tasks/${taskId}`)
  return res.data?.data ?? res.data
}

export async function createTask(columnId: string, title: string) {
  const res = await http.post('/tasks', { column_id: columnId, title })
  return res.data?.data ?? res.data
}

export async function updateTask(taskId: string, payload: object) {
  const res = await http.patch(`/tasks/${taskId}`, payload)
  return res.data?.data ?? res.data
}

export async function deleteTask(taskId: string) {
  await http.delete(`/tasks/${taskId}`)
}

export async function moveTask(taskId: string, columnId: string, position?: number) {
  const res = await http.patch(`/tasks/${taskId}/move`, {
    column_id: columnId,
    position: position ?? 0  // ← tambah ini
  })
  return res.data?.data ?? res.data
}

export async function reorderTask(taskId: string, order: number) {
  const res = await http.patch(`/tasks/${taskId}/reorder`, { order })
  return res.data?.data ?? res.data
}