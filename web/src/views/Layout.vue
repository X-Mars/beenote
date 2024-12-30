<template>
  <el-container class="layout-container">
    <!-- 顶部导航模式 -->
    <template v-if="layoutMode === 'horizontal'">
      <el-header height="60px" class="horizontal-header">
        <div class="header-content">
          <div class="logo horizontal">
            <img src="@/assets/logo.png" alt="logo" class="logo-img">
            <h1>蜜蜂笔记</h1>
          </div>
          
          <el-menu
            :router="true"
            :default-active="route.path"
            mode="horizontal"
            class="horizontal-menu"
          >
            <el-menu-item index="/">
              <el-icon><DataLine /></el-icon>
              <span>仪表盘</span>
            </el-menu-item>
            <el-menu-item index="/notes">
              <el-icon><Document /></el-icon>
              <span>笔记管理</span>
            </el-menu-item>
            <el-menu-item index="/groups">
              <el-icon><FolderOpened /></el-icon>
              <span>分组管理</span>
            </el-menu-item>
          </el-menu>

          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                <el-avatar :size="32" class="avatar">
                  {{ (userStore.user?.name || userStore.user?.username)?.charAt(0).toUpperCase() }}
                </el-avatar>
                <span class="username">{{ userStore.user?.name || userStore.user?.username }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="switchLayout">
                    <el-icon><component :is="layoutMode === 'horizontal' ? 'Expand' : 'Fold'" /></el-icon>
                    切换布局
                  </el-dropdown-item>
                  <el-dropdown-item command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </template>

    <!-- 侧边栏导航模式 -->
    <template v-else>
      <el-aside width="200px">
        <div class="logo">
          <img src="@/assets/logo.png" alt="logo" class="logo-img">
          <h1>蜜蜂笔记</h1>
        </div>
        <el-menu
          :router="true"
          :default-active="route.path"
          class="menu"
        >
          <el-menu-item index="/">
            <el-icon><DataLine /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/notes">
            <el-icon><Document /></el-icon>
            <span>笔记管理</span>
          </el-menu-item>
          <el-menu-item index="/groups">
            <el-icon><FolderOpened /></el-icon>
            <span>分组管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header>
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                <el-avatar :size="32" class="avatar">
                  {{ (userStore.user?.name || userStore.user?.username)?.charAt(0).toUpperCase() }}
                </el-avatar>
                <span class="username">{{ userStore.user?.name || userStore.user?.username }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="switchLayout">
                    <el-icon><component :is="layoutMode === 'vertical' ? 'Fold' : 'Expand'" /></el-icon>
                    切换布局
                  </el-dropdown-item>
                  <el-dropdown-item command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </template>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { 
  DataLine, 
  Document, 
  FolderOpened, 
  ArrowDown,
  Expand,
  Fold,
  SwitchButton
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const layoutMode = ref(localStorage.getItem('layoutMode') || 'vertical')

// 在组件挂载时获取用户信息
onMounted(async () => {
  await userStore.fetchUserInfo()
})

// 监听布局模式变化并保存到本地存储
watch(layoutMode, (newValue) => {
  localStorage.setItem('layoutMode', newValue)
})

const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
  } else if (command === 'switchLayout') {
    layoutMode.value = layoutMode.value === 'vertical' ? 'horizontal' : 'vertical'
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.horizontal-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 0;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

/* 顶部导航模式下，为内容区域添加上边距，避免被固定头部遮挡 */
.layout-container:has(.horizontal-header) .el-main {
  padding-top: 80px;
}

.el-aside {
  height: 100vh;
  background-color: #fff;
  border-right: 1px solid #dcdfe6;
  display: flex;
  flex-direction: column;
}

.menu {
  flex: 1;
  border-right: none;
  overflow-y: auto;
}

.el-header {
  background-color: #fff;
  /* border-bottom: 1px solid #dcdfe6; */
  padding: 0;
  display: flex;
  justify-content: flex-end;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin: 0 auto;
  padding: 0 40px;
  height: 100%;
}

.horizontal-header .header-content {
  max-width: none;
  padding: 0;
}

.horizontal-header .logo {
  padding-left: 40px;
}

.horizontal-header .header-right {
  padding-right: 40px;
}

.header-left {
  display: flex;
  align-items: center;
}

.horizontal-menu {
  flex: 1;
  margin: 0 60px;
  border-bottom: none;
  justify-content: center;
}

.header-right {
  display: flex;
  align-items: center;
  padding-right: 20px;
  height: 100%;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  height: 100%;
}

:deep(.el-dropdown:focus-visible) {
  outline: none;
}

:deep(.el-popper) {
  border: none;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px;
  height: 60px;
}

.logo.horizontal {
  padding-left: 40px;
}

.logo-img {
  width: 32px;
  height: 32px;
}

.logo h1 {
  margin: 0;
  font-size: 20px;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

:deep(.el-menu--horizontal) {
  border-bottom: none;
}

.avatar {
  background-color: var(--el-color-primary);
  color: #fff;
  font-weight: bold;
}

.username {
  font-size: 14px;
  color: var(--el-text-color-regular);
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 调整侧边栏菜单的上边距，与logo对齐 */
.el-aside .el-menu {
  margin-top: 0;
}
</style> 