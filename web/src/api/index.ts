import request from './request'
import type { Note, Group } from './types'

export const login = (data: { username: string; password: string }) => {
  return request.post('/auth/login/', data)
}

export const getNotes = (params?: any) => {
  return request.get<Note[]>('/notes/', { params })
}

export const createNote = (data: Partial<Note>) => {
  return request.post<Note>('/notes/', data)
}

export const updateNote = (id: number, data: Partial<Note>) => {
  return request.patch<Note>(`/notes/${id}/`, data)
}

export const deleteNote = (id: number) => {
  return request.delete(`/notes/${id}/`)
}

export const getGroups = () => {
  return request.get<Group[]>('/groups/')
}

export const createGroup = (data: Partial<Group>) => {
  return request.post<Group>('/groups/', data)
}

export const updateGroup = (id: number, data: Partial<Group>) => {
  return request.patch<Group>(`/groups/${id}/`, data)
}

export const deleteGroup = (id: number) => {
  return request.delete(`/groups/${id}/`)
}

export const getNoteStats = (params?: { range?: string }) => {
  return request.get('/notes/stats/', { params })
}

export const getActiveUsers = () => {
  return request.get('/auth/stats/')
} 