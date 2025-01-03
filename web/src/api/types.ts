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
  id: string
  title: string
  content: string
  group: string | null
  created_at: string
  updated_at: string
  creator?: {
    id: string
    username: string
    name: string
  }
  group_detail?: {
    id: string
    name: string
  }
}

export interface NoteResponse {
  results: Note[]
  count: number
}

export interface User {
  id: string
  username: string
  name: string
  first_name: string
  last_name: string
  email: string
  role: string
  is_active: boolean
  last_active_at: string
  date_joined: string
  notes?: string[]
  note_group?: string[]
  statusLoading?: boolean
  avatar?: string
}

export interface Group {
  id: string
  name: string
  description?: string
  created_at: string
  updated_at: string
  note_count?: number
  creator?: {
    id: string
    username: string
    name: string
  }
}

export interface OAuthUrls {
  wecom_url: string | null
  feishu_url: string | null
  dingtalk_url: string | null
  github_url: string | null
} 