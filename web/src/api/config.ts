import request from './request'

export interface OAuthConfig {
  id: string
  enabled: boolean
  created_at: string
  updated_at: string
}

export interface WeComConfig extends OAuthConfig {
  corp_id: string
  agent_id: string
  secret: string
}

export interface FeiShuConfig extends OAuthConfig {
  app_id: string
  app_secret: string
}

export interface DingTalkConfig extends OAuthConfig {
  client_id: string
  client_secret: string
  app_id: string
}

export interface GitHubConfig extends OAuthConfig {
  client_id: string
  client_secret: string
  redirect_uri: string
}

export const configApi = {
  // 企业微信配置
  getWeComConfigs: () => request.get<WeComConfig[]>('/auth/wecom-config/'),
  createWeComConfig: (data: Partial<WeComConfig>) => request.post<WeComConfig>('/auth/wecom-config/', data),
  updateWeComConfig: (id: string, data: Partial<WeComConfig>) => request.patch<WeComConfig>(`/auth/wecom-config/${id}/`, data),
  deleteWeComConfig: (id: string) => request.delete(`/auth/wecom-config/${id}/`),
  getCurrentWeComConfig: () => request.get<WeComConfig>('/auth/wecom-config/current/'),

  // 飞书配置
  getFeiShuConfigs: () => request.get<FeiShuConfig[]>('/auth/feishu-config/'),
  createFeiShuConfig: (data: Partial<FeiShuConfig>) => request.post<FeiShuConfig>('/auth/feishu-config/', data),
  updateFeiShuConfig: (id: string, data: Partial<FeiShuConfig>) => request.patch<FeiShuConfig>(`/auth/feishu-config/${id}/`, data),
  deleteFeiShuConfig: (id: string) => request.delete(`/auth/feishu-config/${id}/`),
  getCurrentFeiShuConfig: () => request.get<FeiShuConfig>('/auth/feishu-config/current/'),

  // 钉钉配置
  getDingTalkConfigs: () => request.get<DingTalkConfig[]>('/auth/dingtalk-config/'),
  createDingTalkConfig: (data: Partial<DingTalkConfig>) => request.post<DingTalkConfig>('/auth/dingtalk-config/', data),
  updateDingTalkConfig: (id: string, data: Partial<DingTalkConfig>) => request.patch<DingTalkConfig>(`/auth/dingtalk-config/${id}/`, data),
  deleteDingTalkConfig: (id: string) => request.delete(`/auth/dingtalk-config/${id}/`),
  getCurrentDingTalkConfig: () => request.get<DingTalkConfig>('/auth/dingtalk-config/current/'),

  // GitHub配置
  getGitHubConfigs: () => request.get<GitHubConfig[]>('/auth/github-config/'),
  createGitHubConfig: (data: Partial<GitHubConfig>) => request.post<GitHubConfig>('/auth/github-config/', data),
  updateGitHubConfig: (id: string, data: Partial<GitHubConfig>) => request.patch<GitHubConfig>(`/auth/github-config/${id}/`, data),
  deleteGitHubConfig: (id: string) => request.delete(`/auth/github-config/${id}/`),
  getCurrentGitHubConfig: () => request.get<GitHubConfig>('/auth/github-config/current/')
} 