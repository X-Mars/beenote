/* eslint-disable no-useless-catch */
import { defineStore } from 'pinia'
import type { User } from '@/api/types'
import { userApi } from '@/api/users'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    token: localStorage.getItem('token'),
    refreshToken: localStorage.getItem('refreshToken'),
    initialized: false
  }),
  
  getters: {
    isAdmin: (state) => state.user?.role === 'admin',
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    setUser(user: User) {
      this.user = user
      localStorage.setItem('user', user)
    },
    
    setToken(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },

    setRefreshToken(refreshToken: string) {
      this.refreshToken = refreshToken
      localStorage.setItem('refreshToken', refreshToken)
    },
    
    clearUser() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    async fetchUserInfo() {
      try {
        const res = await userApi.getUserInfo()
        this.user = res.data
        this.setUser(res.data)
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.clearUser()
        throw error
      }
    },

    logout() {
      this.clearUser()
    },

    async initialize() {
      if (this.token && !this.initialized) {
        try {
          await this.fetchUserInfo()
        } catch (error) {
          console.error('初始化用户信息失败:', error)
        } finally {
          this.initialized = true
        }
      } else {
        this.initialized = true
      }
    },

    async login(username: string, password: string) {
      try {
        const response = await userApi.login({ username, password })
        this.setToken(response.data.access)
        this.setRefreshToken(response.data.refresh)
        this.setUser(response.data.user)
        return response
      } catch (error) {
        throw error
      }
    },

    async wecomLogin(code: string) {
      try {
        const response = await userApi.wecomLogin(code)
        this.setToken(response.data.access)
        this.setRefreshToken(response.data.refresh)
        this.setUser(response.data.user)
        return response
      } catch (error) {
        throw error
      }
    },
       
    async feishuLogin(code: string) {
      try {
        const response = await userApi.feishuLogin(code)
        this.setToken(response.data.access)
        this.setRefreshToken(response.data.refresh)
        this.setUser(response.data.user)
        return response
      } catch (error) {
        throw error
      }
    },

    async dingtalkLogin(authCode: string) {
      try {
        const response = await userApi.dingtalkLogin(authCode)
        this.setToken(response.data.access)
        this.setRefreshToken(response.data.refresh)
        this.setUser(response.data.user)
        return response
      } catch (error) {
        throw error
      }
    },
  }
}) 