/// <reference types="vite/client" /> 

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    roles?: string[]
    title?: string
    icon?: Component
    hidden?: boolean
  }
} 