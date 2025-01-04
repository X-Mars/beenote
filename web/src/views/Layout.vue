<template>
  <el-container class="layout-container layout-wrapper">
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
            <template v-for="item in filteredMenuItems" :key="item.path">
              <el-sub-menu 
                v-if="getVisibleChildren(item).length > 1"
                :index="item.path"
              >
                <template #title>
                  <el-icon>
                    <component :is="item.meta?.icon" v-if="item.meta?.icon" />
                  </el-icon>
                  <span>{{ item.meta?.title }}</span>
                </template>
                <el-menu-item 
                  v-for="child in getVisibleChildren(item)"
                  :key="child.path"
                  :index="child.path"
                >
                  <el-icon>
                    <component :is="child.meta?.icon" v-if="child.meta?.icon" />
                  </el-icon>
                  <span>{{ child.meta?.title }}</span>
                </el-menu-item>
              </el-sub-menu>
              <el-menu-item 
                v-else 
                :index="getVisibleChildren(item).length === 1 ? getVisibleChildren(item)[0].path : item.path"
              >
                <el-icon>
                  <component 
                    :is="getVisibleChildren(item).length === 1 
                      ? getVisibleChildren(item)[0].meta?.icon 
                      : item.meta?.icon" 
                    v-if="getVisibleChildren(item).length === 1 
                      ? getVisibleChildren(item)[0].meta?.icon 
                      : item.meta?.icon"
                  />
                </el-icon>
                <span>{{ getVisibleChildren(item).length === 1 
                  ? getVisibleChildren(item)[0].meta?.title 
                  : item.meta?.title }}</span>
              </el-menu-item>
            </template>
          </el-menu>

          <div class="header-right">
            <a href="https://qm.qq.com/cgi-bin/qm/qr?k=a_y5qjuIfBYZHkhGg4JTZqGjTk3KUI5T&jump_from=webapi&authKey=qJpb8UQWFJcxKBdT/zq9kGBqiMxOm9k3TkfYeAtaVtHAbKbIfxMiGBolmP+aWa5b" target="_blank">
              <el-tooltip content="加入QQ摸鱼群" placement="bottom">
                <img width="32px" src="@/assets/qq.png" style="margin-right: 16px; background-color: #fff;"/>
              </el-tooltip>
            </a>
            <a href="https://github.com/X-Mars/beenote" target="_blank">
              <el-tooltip content="访问 火星小刘的 GitHub 仓库" placement="bottom">
                <img width="32px" src="@/assets/github.png" style="margin-right: 16px; background-color: #fff;"/>
              </el-tooltip>
            </a>
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                <img width="32px" :src="userStore.user?.avatar || '/src/assets/logo.png'" style="margin-right: 16px; background-color: #fff;"/>
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
      <div class="sub-header">
        <tag-nav />
      </div>
      <el-main class="main-content">
        <router-view />
      </el-main>
      <el-footer height="30px" class="footer">
        <div class="footer-content">
          <span>© {{ new Date().getFullYear() }} 
            <a href="https://github.com/X-Mars" target="_blank" class="author-link">火星小刘</a>
          </span>
        </div>
      </el-footer>
    </template>

    <!-- 侧边栏导航模式 -->
    <template v-else>
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <img src="@/assets/logo.png" alt="logo" class="logo-img">
          <h1>蜜蜂笔记</h1>
        </div>
        <el-menu
          :router="true"
          :default-active="route.path"
          class="menu"
        >
          <template v-for="item in filteredMenuItems" :key="item.path">
            <el-sub-menu 
              v-if="getVisibleChildren(item).length > 1"
              :index="item.path"
            >
              <template #title>
                <el-icon><component :is="item.meta?.icon" /></el-icon>
                <span>{{ item.meta?.title }}</span>
              </template>
              <el-menu-item 
                v-for="child in getVisibleChildren(item)"
                :key="child.path"
                :index="child.path"
              >
                <el-icon><component :is="child.meta?.icon" /></el-icon>
                <span>{{ child.meta?.title }}</span>
              </el-menu-item>
            </el-sub-menu>
            <el-menu-item 
              v-else 
              :index="getVisibleChildren(item).length === 1 ? getVisibleChildren(item)[0].path : item.path"
            >
              <el-icon>
                <component :is="getVisibleChildren(item).length === 1 
                  ? getVisibleChildren(item)[0].meta?.icon 
                  : item.meta?.icon" 
                />
              </el-icon>
              <span>{{ getVisibleChildren(item).length === 1 
                ? getVisibleChildren(item)[0].meta?.title 
                : item.meta?.title }}</span>
            </el-menu-item>
          </template>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header class="vertical-header">
          <div class="header-right">
            <a href="https://qm.qq.com/cgi-bin/qm/qr?k=a_y5qjuIfBYZHkhGg4JTZqGjTk3KUI5T&jump_from=webapi&authKey=qJpb8UQWFJcxKBdT/zq9kGBqiMxOm9k3TkfYeAtaVtHAbKbIfxMiGBolmP+aWa5b" target="_blank">
              <el-tooltip content="加入QQ摸鱼群" placement="bottom">
                <img width="32px" src="@/assets/qq.png" style="margin-right: 16px; background-color: #fff;"/>
              </el-tooltip>
            </a>
            <a href="https://github.com/X-Mars/beenote" target="_blank">
              <el-tooltip content="访问 火星小刘的 GitHub 仓库" placement="bottom">
                <img width="32px" src="@/assets/github.png" style="margin-right: 16px; background-color: #fff;"/>
              </el-tooltip>
            </a>
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                <img width="32px" :src="userStore.user?.avatar || '/src/assets/logo.png'" style="margin-right: 16px; background-color: #fff;"/>
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
          <tag-nav />
        </el-header>
        
        <el-main>
          <router-view />
        </el-main>
        <el-footer height="30px" class="footer">
          <div class="footer-content">
            <span>© {{ new Date().getFullYear() }} 
              <a href="https://github.com/X-Mars" target="_blank" class="author-link">火星小刘</a>
            </span>
          </div>
        </el-footer>
      </el-container>
    </template>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import TagNav from '@/components/TagNav.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const layoutMode = ref(localStorage.getItem('layoutMode') || 'horizontal')

// 获取可见的子路由
const getVisibleChildren = (route: RouteRecordRaw) => {
  return (route.children || []).filter(child => !child.meta?.hidden)
}

// 根据用户角色过滤菜单
const filteredMenuItems = computed(() => {
  // 获取根路由的子路由（排除登录页）
  const menuRoutes = router.options.routes.filter(route => 
    route.path !== '/login' && route.children
  )
  
  // 过滤需要权限的路由
  return menuRoutes.filter(route => {
    if (route.meta?.roles) {
      return route.meta.roles.includes(userStore.user?.role || '')
    }
    return true
  })
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

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    await userStore.initialize()
  } catch (error) {
    console.error('获取用户信息失败:', error)
    userStore.clearUser()
    router.push('/login')
  }
}

// 在组件挂载时获取用户信息
onMounted(() => {
  if (userStore.token) {
    fetchUserInfo()
  }
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
  overflow-x: hidden;
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
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
  height: 60px !important;
}

/* 顶部导航模式下的标签导航容器 */
.sub-header {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  z-index: 999;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

/* 顶部导航模式下，为内容区域添加上边距，避免被固定头部遮挡 */
.layout-container:has(.horizontal-header) .el-main {
  padding-top: 110px;  /* 增加内容区域的上边距，为标签导航留出空间 */
}

.el-aside {
  height: 100vh;
  background-color: #fff;
  border-right: 1px solid #dcdfe6;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.menu {
  flex: 1;
  border-right: none;
  overflow-y: auto;
}

.el-header {
  height: auto !important;
  padding: 0;
  background-color: #fff;
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
  padding: 0 20px;
  height: 48px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
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

/* 侧边栏模式下的 header 样式 */
.el-container:not(:has(.horizontal-header)) .el-header {
  height: auto !important;
  padding: 0;
  background-color: #fff;
}

/* 调整标签导航样式 */
:deep(.tag-nav) {
  border-bottom: 1px solid var(--el-border-color-light);
}

/* 确保内容区域不被遮挡 */
.el-main {
  overflow-x: hidden;
  overflow-y: auto;
  height: calc(100vh - 160px);
  padding: 0;
  box-sizing: border-box;
  
  /* 自定义滚动条样式 */
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-track {
    background-color: transparent;
  }
}

.github-icon {
  width: 24px;
  height: 24px;
  margin-right: 16px;
  cursor: pointer;
}

.header-right {
  display: flex;
  align-items: center;
}

.footer {
  background-color: #fff;
  border-top: 1px solid var(--el-border-color-light);
  margin-top: auto;
  flex-shrink: 0;  /* 防止 footer 被压缩 */
  position: fixed;
  bottom: 0;
  width: 100%;
  z-index: 1000;
  left: 0;
  right: 0;
}

/* 侧边栏模式下的 footer 样式 */
.layout-container:not(:has(.horizontal-header)) .footer {
  width: calc(100% - 200px);
  margin-left: 200px;
}

.footer-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.layout-wrapper {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  overflow-y: hidden;
}

.main-content {
  overflow-x: hidden;
  overflow-y: auto;
  height: calc(100vh - 160px);
  padding: 0;
  box-sizing: border-box;
  
  /* 自定义滚动条样式 */
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-track {
    background-color: transparent;
  }
}

.sidebar {
  background-color: #fff;
  border-right: 1px solid var(--el-border-color-light);
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  overflow-x: hidden;
  overflow-y: overlay;
  
  /* 自定义滚动条样式 */
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-track {
    background-color: transparent;
  }
}

/* 侧边栏模式下的容器样式 */
.layout-container:not(:has(.horizontal-header)) > .el-container {
  margin-left: 200px;
  width: calc(100% - 200px);
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 侧边栏模式下的头部样式 */
.vertical-header {
  background-color: #fff;
  border-bottom: 1px solid var(--el-border-color-light);
  position: sticky;
  top: 0;
  z-index: 999;
  flex-shrink: 0;  /* 防止头部被压缩 */
}

/* 内容容器样式 */
.el-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* 添加作者链接样式 */
.author-link {
  color: var(--el-text-color-secondary);
  text-decoration: none;
  transition: color 0.3s;
}

.author-link:hover {
  color: var(--el-color-primary);
}
</style> 