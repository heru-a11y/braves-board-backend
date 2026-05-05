// src/services/columnService.ts
import axios from 'axios'

const http = axios.create({ baseURL: 'http://localhost:8000' })
http.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
})

export async function getColumns(boardId: string) {
    const res = await http.get('/columns', { params: { board_id: boardId } })
    return res.data?.data ?? res.data ?? []
}

// columnService.ts
export async function createColumn(boardId: string, title: string) {
    try {
        const res = await http.post('/columns', { title, board_id: boardId })
        return res.data?.data ?? res.data
    } catch (e: any) {
        console.log('create column error detail:', e.response?.data) // ← tambah ini
        throw e
    }
}

export async function updateColumn(columnId: string, payload: { title?: string; order?: number }) {
    const res = await http.patch(`/columns/${columnId}`, payload)
    return res.data?.data ?? res.data
}

export async function deleteColumn(columnId: string) {
    await http.delete(`/columns/${columnId}`)
}

export async function reorderColumn(columnId: string, newOrder: number) {
    const res = await http.patch(`/columns/${columnId}/reorder`, { order: newOrder })
    return res.data?.data ?? res.data
}