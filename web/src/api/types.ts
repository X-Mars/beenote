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
  name?: string
  first_name: string
  last_name: string
  email: string
  role: string
  is_active: boolean
  last_active_at: string
  date_joined: string
  notes?: number[]
  note_group?: number[]
  statusLoading?: boolean
} 