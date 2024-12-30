import { defineStore } from 'pinia'
import type { User } from '@/api/types'
import request from '@/api/request'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    token: localStorage.getItem('token'),
    initialized: false
  }),
  
  getters: {
    isAdmin: (state) => state.user?.role === 'admin',
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    setUser(user: User) {
      this.user = user
    },
    
    setToken(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    clearUser() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    async fetchUserInfo() {
      try {
        const res = await request.get('/auth/me/')
        this.user = res.data
        localStorage.setItem('user', JSON.stringify(res.data))
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
    }
  }
}) 