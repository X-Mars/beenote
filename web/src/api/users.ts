import request from './request'
import type { User } from './types'

export interface LoginResponse {
  access: string
  refresh: string
  user: User
}

export interface LoginParams {
  username: string
  password: string
}

export interface GitLabUser {
  id: string
  name: string
  username: string
  email: string
  avatar_url: string
  gitlab_id: string
  created_at: string
  updated_at: string
}

export interface GiteeUser {
  id: string
  name: string
  username: string
  email: string
  avatar_url: string
  gitee_id: string
  created_at: string
  updated_at: string
}

export const userApi = {
  // 用户登录
  login: (data: LoginParams) => {
    return request.post<LoginResponse>('/auth/login/', data)
  },

  // 获取用户信息
  getUserInfo: () => {
    return request.get<User>('/auth/me/')
  },

  // 企业微信登录
  wecomLogin: (code: string) => {
    return request.post<LoginResponse>('/auth/wecom/login/', { code })
  },

  // 飞书登录
  feishuLogin: (code: string) => {
    return request.post<LoginResponse>('/auth/feishu/login/', { code })
  },

  // 钉钉登录
  dingtalkLogin: (authCode: string) => {
    return request.post<LoginResponse>('/auth/dingtalk/login/', { authCode })
  },

  // GitHub登录
  githubLogin: (code: string) => {
    return request.post<LoginResponse>('/auth/github/login/', { code })
  },

  // Google登录
  googleLogin: (code: string) => {
    return request.post<LoginResponse>('/auth/google/login/', { code })
  },

  // GitLab登录
  gitlabLogin: (code: string) => {
    return request.post<LoginResponse>('/auth/gitlab/login/', { code })
  },

  // Gitee登录
  giteeLogin: (code: string) => {
    return request.post<LoginResponse>('/auth/gitee/login/', { code })
  },

  // 获取第三方登录二维码
  getLoginQRCode: () => {
    return request.get<{
      wecom_url: string | null
      feishu_url: string | null
      dingtalk_url: string | null
      github_url: string | null
      google_url: string | null
      gitlab_url: string | null
      gitee_url: string | null
    }>('/auth/login/qrcode/')
  }
}
