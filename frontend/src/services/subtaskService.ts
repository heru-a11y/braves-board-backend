import axios from 'axios'

const http = axios.create({ baseURL: 'http://localhost:8000' })
http.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export async function createSubtask(taskId: string, title: string) {
  const res = await http.post(`/tasks/${taskId}/subtasks`, { title })
  return res.data?.data ?? res.data
}

export async function updateSubtask(subtaskId: string, payload: { title?: string }) {
  const res = await http.patch(`/subtasks/${subtaskId}`, payload)
  return res.data?.data ?? res.data
}

export async function deleteSubtask(subtaskId: string) {
  await http.delete(`/subtasks/${subtaskId}`)
}

export async function completeSubtask(subtaskId: string) {
  const res = await http.patch(`/subtasks/${subtaskId}/complete`)
  return res.data?.data ?? res.data
}

export async function moveSubtask(subtaskId: string, taskId: string, position: number) {
  const res = await http.patch(`/subtasks/${subtaskId}/move`, { task_id: taskId, position })
  return res.data?.data ?? res.data
}