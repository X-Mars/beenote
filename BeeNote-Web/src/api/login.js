import request from '@/utils/request'

export function loginByUsername(username, password) {
  const data = {
    username,
    password
  }
  return request({
    url: '/api-v1/login/',
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url: '/api-v1/logout/',
    method: 'get'
  })
}

export function getUserInfo(token) {
  return request({
    url: '/api-v1/userinfo/',
    method: 'get',
    params: { token }
  })
}

