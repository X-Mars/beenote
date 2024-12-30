import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'
import { 
  DataLine, 
  Document, 
  Lock,
  Edit,
  View,
  User,
  FolderOpened,
  Notebook
} from '@element-plus/icons-vue'
import type { Component } from 'vue'

// 扩展 RouteMeta 类型
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    roles?: string[]
    title?: string
    icon?: Component
    hidden?: boolean
  }
}

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    meta: {
      requiresAuth: true,
      title: '仪表盘',
      icon: DataLine
    },
    children: [
      {
        path: '/',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: {
          title: '仪表盘',
          icon: DataLine
        }
      }
    ]
  },
  {
    path: '/notes',
    name: 'NotesIndex',
    component: () => import('@/views/Layout.vue'),
    meta: {
      title: '笔记管理',
      icon: Document
    },
    children: [
      {
        path: '/notes',
        name: 'Note',
        component: () => import('@/views/Notes.vue'),
        meta: {
          title: '笔记管理',
          icon: Document
        }
      },
      {
        path: '/notes/edit/:id?',
        name: 'NoteEdit',
        component: () => import('@/views/NoteEdit.vue'),
        meta: {
          title: '编辑笔记',
          icon: Edit,
          hidden: true  // 在导航菜单中隐藏
        }
      },
      {
        path: '/notes/view/:id',
        name: 'NoteView',
        component: () => import('@/views/NoteView.vue'),
        meta: {
          title: '查看笔记',
          icon: View,
          hidden: true  // 在导航菜单中隐藏
        }
      }
    ]
  },
  {
    path: '/groups',
    component: () => import('@/views/Layout.vue'),
    meta: {
      requiresAuth: true,
      title: '笔记分组',
      icon: Notebook
    },
    children: [
      {
        path: '/groups',
        name: 'NoteGroup',
        component: () => import('@/views/Groups.vue'),
        meta: {
          title: '笔记分组',
          icon: Notebook
        }
      }
    ]
  },
  {
    path: '/auth/users',
    name: 'Auth',
    component: () => import('@/views/Layout.vue'),
    meta: { 
      title: '权限管理',
      icon: Lock,
      roles: ['admin']
    },
    children: [
      {
        path: '/auth/users',
        name: 'Users',
        component: () => import('@/views/auth/Users.vue'),
        meta: {
          title: '用户管理',
          icon: User
        }
      },
      {
        path: '/auth/groups',
        name: 'AuthGroups',
        component: () => import('@/views/auth/Groups.vue'),
        meta: {
          title: '分组管理',
          icon: FolderOpened
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const token = localStorage.getItem('token')

  // 等待用户信息初始化
  await userStore.initialize()

  if (to.meta.requiresAuth && !token) {
    // 需要登录但未登录，跳转到登录页
    next('/login')
  } else if (to.meta.roles && !to.meta.roles.includes(userStore.user?.role)) {
    // 需要特定角色权限但没有权限，重定向到首页
    next('/')
  } else {
    next()
  }
})

export default router 
