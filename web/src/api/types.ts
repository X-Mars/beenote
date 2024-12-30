export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

export interface PaginatedResponse<T> {
  results: T[]
  count: number
}

export interface Note {
  id: number
  title: string
  content: string
  group: number | null
  created_at: string
  updated_at: string
  creator?: {
    id: number
    username: string
    name: string
  }
  group_detail?: {
    id: number
    name: string
  }
}

export interface NoteResponse {
  results: Note[]
  count: number
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

export interface Group {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
  note_count?: number
  creator?: {
    id: number
    username: string
    name: string
  }
} 