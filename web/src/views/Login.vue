<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-content">
        <div class="login-left">
          <div class="welcome-text">
            <h1>蜜蜂🐝笔记</h1>
            <p>便捷记录、高效管理、安全可靠</p>
          </div>
          <div class="decoration">
            <el-icon class="icon-note"><Notebook /></el-icon>
            <div class="circle circle-1"></div>
            <div class="circle circle-2"></div>
            <div class="circle circle-3"></div>
          </div>
        </div>
        
        <div class="login-right">
          <el-card class="login-card">
            <template #header>
              <div class="card-header">
                <img src="@/assets/logo.png" class="logo" alt="logo">
                <h2>用户登录</h2>
              </div>
            </template>
            
            <el-form 
              :model="loginForm" 
              :rules="rules" 
              ref="loginFormRef"
              class="login-form"
            >
              <el-form-item prop="username">
                <el-input 
                  v-model="loginForm.username" 
                  placeholder="用户名"
                  :prefix-icon="User"
                  size="large"
                />
              </el-form-item>
              
              <el-form-item prop="password">
                <el-input 
                  v-model="loginForm.password" 
                  type="password" 
                  placeholder="密码"
                  :prefix-icon="Lock"
                  size="large"
                  show-password
                />
              </el-form-item>
              
              <div class="form-footer">
                <el-checkbox v-model="rememberMe">记住我</el-checkbox>
                <el-link type="primary">忘记密码？</el-link>
              </div>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  @click="handleLogin" 
                  :loading="loading" 
                  class="login-button"
                  size="large"
                >
                  登录
                </el-button>
              </el-form-item>
              
              <!-- 第三方登录 -->
              <div class="third-party-login">
                <div class="divider">
                  <span>其他登录方式</span>
                </div>
                <div class="login-icons">
                  <el-tooltip content="企业微信登录" placement="top">
                    <div class="login-icon" @click="handleThirdPartyLogin(qrcodeUrls.wecom_url)">
                      <img src="@/assets/wecom.png" alt="企业微信">
                    </div>
                  </el-tooltip>
                  <el-tooltip content="飞书登录" placement="top">
                    <div class="login-icon" @click="handleThirdPartyLogin(qrcodeUrls.feishu_url)">
                      <img src="@/assets/feishu.png" alt="飞书">
                    </div>
                  </el-tooltip>
                  <el-tooltip content="钉钉登录" placement="top">
                    <div class="login-icon" @click="handleThirdPartyLogin(qrcodeUrls.dingtalk_url)">
                      <img src="@/assets/dingtalk.png" alt="钉钉">
                    </div>
                  </el-tooltip>
                </div>
              </div>
            </el-form>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { User, Lock, Notebook } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import { userApi } from '@/api/users'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const loginFormRef = ref<FormInstance>()
const loading = ref(false)
const rememberMe = ref(false)
const qrcodeUrls = ref({
  wecom_url: null,
  feishu_url: null,
  dingtalk_url: null
})

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        console.log(loginForm)
        await userStore.login(loginForm.username, loginForm.password)
        
        if (rememberMe.value) {
          localStorage.setItem('username', loginForm.username)
        } else {
          localStorage.removeItem('username')
        }
        
        router.push('/')
      } catch (error) {
        ElMessage.error('登录失败：' + (error as Error).message)
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}

// 检查是否有保存的用户名
const savedUsername = localStorage.getItem('username')
if (savedUsername) {
  loginForm.username = savedUsername
  rememberMe.value = true
}

// 获取第三方登录二维码URL
const fetchQRCodeUrls = async () => {
  try {
    const res = await userApi.getLoginQRCode()
    qrcodeUrls.value = res.data
  } catch (error) {
    console.error('获取第三方登录二维码失败:', error)
  }
}

// 处理第三方登录点击
const handleThirdPartyLogin = (url: string | null) => {
  if (url) {
    window.location.href = url
  } else {
    ElMessage.warning('该登录方式未配置')
  }
}

onMounted(() => {
  fetchQRCodeUrls()
  const { username, password } = route.query
  if (username) {
    loginForm.username = username as string
  }
  if (password) {
    loginForm.password = password as string
  }
  // if (username && password) {
  //   handleLogin()
  // }
})
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #e0f2ff 0%, #f5f7fa 100%);
  overflow: hidden;
}

.login-content {
  display: flex;
  width: 900px;
  height: 600px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.login-left {
  flex: 1;
  background: linear-gradient(135deg, var(--el-color-primary) 0%, var(--el-color-primary-light-3) 100%);
  padding: 40px;
  position: relative;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.welcome-text {
  position: relative;
  z-index: 1;
}

.welcome-text h1 {
  font-size: 36px;
  margin: 0 0 10px 0;
  font-weight: 600;
}

.welcome-text h2 {
  font-size: 28px;
  margin: 0 0 20px 0;
  font-weight: 500;
}

.welcome-text p {
  font-size: 16px;
  opacity: 0.9;
  margin: 0;
}

.decoration {
  position: absolute;
  bottom: 40px;
  right: 40px;
}

.icon-note {
  font-size: 120px;
  opacity: 0.2;
  animation: float 6s ease-in-out infinite;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.circle-1 {
  width: 100px;
  height: 100px;
  top: -20px;
  left: -20px;
  animation: float 8s ease-in-out infinite;
}

.circle-2 {
  width: 60px;
  height: 60px;
  bottom: 40px;
  left: 20px;
  animation: float 6s ease-in-out infinite 1s;
}

.circle-3 {
  width: 40px;
  height: 40px;
  top: 40px;
  right: 40px;
  animation: float 4s ease-in-out infinite 0.5s;
}

.login-right {
  flex: 1;
  padding: 40px;
  display: flex;
  align-items: center;
  width: 100%;
}

.login-card {
  width: 100%;
  border: none;
  box-shadow: none;
}

.card-header {
  text-align: center;
  /* margin-bottom: 20px; */
}

.logo {
  width: 100px;
  height: 100px;
  margin-bottom: 16px;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

:deep(.el-card) {
  /* 去掉登录框周围阴影 */
  box-shadow: none !important;
  /* 圆角 */
  border-radius: 80px;
}

:deep(.el-card__header) {
  border-bottom: none;
  padding-bottom: 0;
}

.login-form {
  padding: 20px 0;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  border-radius: 22px;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-content {
    width: 100%;
    height: 100%;
    flex-direction: column;
    border-radius: 0;
  }
  
  .login-left {
    padding: 20px;
    height: 200px;
  }
  
  .welcome-text h1 {
    font-size: 28px;
  }
  
  .welcome-text h2 {
    font-size: 24px;
  }
  
  .icon-note {
    font-size: 80px;
  }
  
  .login-right {
    padding: 20px;
  }
}

.third-party-login {
  margin-top: 20px;
  text-align: center;
}

.divider {
  position: relative;
  margin: 20px 0;
  text-align: center;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 35%;
  height: 1px;
  background-color: #dcdfe6;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider span {
  background-color: white;
  padding: 0 10px;
  color: #909399;
  font-size: 14px;
}

.login-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.login-icon {
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: transform 0.2s;
}

.login-icon:hover {
  transform: scale(1.1);
}

.login-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
