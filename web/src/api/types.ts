export interface Note {
  id: number
  title: string
  content: string
  group: number
  created_at: string
  updated_at: string
}

export interface Group {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface User {
  id: number
  username: string
  role: string
} 