import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import request from '@/api/request'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const res = await request.get('/auth/me/')
      user.value = res.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  // 设置用户信息
  const setUser = (userInfo: User) => {
    user.value = userInfo
  }

  // 设置 token
  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  // 退出登录
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    setUser,
    setToken,
    logout,
    fetchUserInfo
  }
}) 