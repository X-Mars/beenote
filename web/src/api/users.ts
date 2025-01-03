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

  // 获取第三方登录二维码
  getLoginQRCode: () => {
    return request.get<{
      wecom_url: string | null
      feishu_url: string | null
      dingtalk_url: string | null
      github_url: string | null
    }>('/auth/login/qrcode/')
  }
} 