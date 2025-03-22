<template>
  <div class="oauth-callback">
    <el-card class="callback-card">
      <template #header>
        <div class="card-header">
          <h2>{{ title }}</h2>
        </div>
      </template>
      <div class="callback-content">
        <el-result
          :icon="loading ? 'info' : (error ? 'error' : 'success')"
          :title="message"
          :sub-title="subMessage"
        >
          <template #extra>
            <el-button type="primary" @click="goToHome" :disabled="loading">
              返回首页
            </el-button>
          </template>
        </el-result>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const error = ref(false)
const message = ref('正在处理登录请求...')
const subMessage = ref('请稍候')

// 根据state获取平台名称
const platformName = computed(() => {
  const stateMap: { [key: string]: string } = {
    'wecom': '企业微信',
    'feishu': '飞书',
    'dingtalk': '钉钉',
    'github': 'GitHub',
    'google': 'Google',
    'gitlab': 'GitLab',
    'gitee': 'Gitee'
  }
  return stateMap[route.query.state as string] || '未知平台'
})

const title = computed(() => `${platformName.value}登录`)

// 处理登录
const handleLogin = async () => {
  try {
    const code = route.query.code
    const authCode = route.query.authCode
    const state = route.query.state?.toLowerCase()
    console.log('code:', code)
    console.log('authCode:', authCode)
    console.log('state:', state)

    if (!code || !state || (!authCode && state === 'dingtalk' && state !== 'github')) {
      throw new Error('缺少必要的参数')
    }

    let response
    switch (state) {
      case 'wecom':
        response = await userStore.wecomLogin(code as string)
        break
      case 'feishu':
        response = await userStore.feishuLogin(code as string)
        break
      case 'dingtalk':
        response = await userStore.dingtalkLogin(authCode as string)
        break
      case 'github':
        response = await userStore.githubLogin(code as string)
        break
      case 'google':
        response = await userStore.googleLogin(code as string)
        break
      case 'gitlab':
        response = await userStore.gitlabLogin(code as string)
        break
      case 'gitee':
        response = await userStore.giteeLogin(code as string)
        break
      default:
        throw new Error('未知的登录类型')
    }

    loading.value = false
    message.value = '登录成功'
    subMessage.value = '正在跳转...'
    
    // 延迟跳转，让用户看到成功提示
    setTimeout(() => {
      router.push('/')
    }, 1000)

  } catch (err: any) {
    loading.value = false
    error.value = true
    message.value = '登录失败'
    subMessage.value = err.message || '请稍后重试'
    ElMessage.error(err.message || '登录失败')
  }
}

const goToHome = () => {
  router.push('/')
}

onMounted(() => {
  handleLogin()
})
</script>

<style scoped>
.oauth-callback {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.callback-card {
  width: 100%;
  max-width: 600px;
  margin: 20px;
}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
}

.callback-content {
  padding: 20px 0;
}
</style> 