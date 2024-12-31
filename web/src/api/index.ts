import request from './request'
import type { Note, Group, User } from './types'

export const login = (data: { username: string; password: string }) => {
  return request.post('/auth/login/', data)
}

export const getNotes = (params?: any) => {
  return request.get<Note[]>('/notes/', { params })
}

export const createNote = (data: Partial<Note>) => {
  return request.post<Note>('/notes/', data)
}

export const updateNote = (id: string, data: Partial<Note>) => {
  return request.patch<Note>(`/notes/${id}/`, data)
}

export const deleteNote = (id: string) => {
  return request.delete(`/notes/${id}/`)
}

export const getGroups = () => {
  return request.get<Group[]>('/groups/')
}

export const createGroup = (data: Partial<Group>) => {
  return request.post<Group>('/groups/', data)
}

export const updateGroup = (id: string, data: Partial<Group>) => {
  return request.patch<Group>(`/groups/${id}/`, data)
}

export const deleteGroup = (id: string) => {
  return request.delete(`/groups/${id}/`)
}

export const getNoteStats = (params?: { range?: string }) => {
  return request.get('/notes/stats/', { params })
}

export const getActiveUsers = () => {
  return request.get('/auth/stats/')
}

export const getNote = (id: string) => {
  return request.get<Note>(`/notes/${id}/`)
}

export const getUsers = () => {
  return request.get<User[]>('/auth/users/')
}

export const createUser = (data: Partial<User>) => {
  return request.post<User>('/auth/users/', data)
}

export const updateUser = (id: string, data: Partial<User>) => {
  return request.patch<User>(`/auth/users/${id}/`, data)
}

export const deleteUser = (id: string) => {
  return request.delete(`/auth/users/${id}/`)
}

export const getAuthGroups = () => {
  return request.get<Group[]>('/auth/groups/')
}

export const createAuthGroup = (data: Partial<Group>) => {
  return request.post<Group>('/auth/groups/', data)
}

export const updateAuthGroup = (id: string, data: Partial<Group>) => {
  return request.patch<Group>(`/auth/groups/${id}/`, data)
}

export const deleteAuthGroup = (id: string) => {
  return request.delete(`/auth/groups/${id}/`)
} 