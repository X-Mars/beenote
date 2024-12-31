import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 5000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 处理后端返回的错误信息
    if (error.response?.data) {
      const errors = error.response.data
      // 如果是对象格式的错误信息，将所有错误信息拼接起来
      if (typeof errors === 'object' && !Array.isArray(errors)) {
        const errorMessages = Object.entries(errors)
          .map(([field, messages]) => {
            // messages 可能是字符串数组
            const msgList = Array.isArray(messages) ? messages : [messages]
            return msgList.join('、')
          })
          .join('；')
        ElMessage.error(errorMessages || '请求失败')
      } else {
        // 如果是其他格式的错误信息
        ElMessage.error(error.response.data.message || '请求失败')
      }
    } else {
      ElMessage.error('请求失败')
    }
    return Promise.reject(error)
  }
)

export default request 