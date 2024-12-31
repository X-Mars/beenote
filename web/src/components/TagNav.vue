<template>
  <div class="tag-nav">
    <el-scrollbar class="scroll-container">
      <el-tag
        v-for="item in visitedViews"
        :key="item.path"
        :type="isActive(item) ? '' : 'info'"
        :effect="isActive(item) ? 'dark' : 'plain'"
        :class="{ active: isActive(item) }"
        round
        closable
        @click="handleClick(item)"
        @close="removeTab(item.path)"
      >
        {{ item.title }}
      </el-tag>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getNote } from '@/api'

interface TagView {
  title: string
  path: string
  params?: Record<string, any>
  name?: string
}

const route = useRoute()
const router = useRouter()
const visitedViews = ref<TagView[]>([])

// 判断标签是否激活
const isActive = (tag: TagView) => {
  return tag.path === route.path
}

// 添加标签
const addView = async (route: any) => {
  const { path, meta, params, name } = route
  if (meta?.title) {
    let title = meta.title as string
    if (route.name === 'NoteView' && params.id) {
      try {
        const res = await getNote(Number(params.id))
        title = res.data.title
      } catch (error) {
        console.error('获取笔记标题失败:', error)
      }
    }
    
    const view: TagView = {
      title,
      path: path,
      params,
      name
    }
    if (!visitedViews.value.some(v => v.path === path)) {
      visitedViews.value.push(view)
    }
  }
}

// 移除标签
const removeTab = (targetPath: string) => {
  const tabs = visitedViews.value
  let activePath = route.path
  if (activePath === targetPath) {
    tabs.forEach((tab, index) => {
      if (tab.path === targetPath) {
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activePath = nextTab.path
        }
      }
    })
  }
  visitedViews.value = tabs.filter(tab => tab.path !== targetPath)
  if (activePath && activePath !== route.path) {
    router.push(activePath)
  }
}

// 处理标签点击
const handleClick = (tag: TagView) => {
  if (tag.name && tag.params) {
    router.push({
      name: tag.name,
      params: tag.params
    })
  } else {
    router.push(tag.path)
  }
}

// 监听路由变化
watch(
  () => route.path,
  async () => {
    await addView(route)
  },
  { immediate: true }
)
</script>

<style scoped>
.tag-nav {
  padding: 4px 0;
  background: #fff;
  border-bottom: 1px solid var(--el-border-color-light);
}

.scroll-container {
  white-space: nowrap;
  padding: 0 10px;
  position: relative;
  overflow: hidden;
  width: 100%;
}

.el-tag {
  margin-right: 4px;
  cursor: pointer;
  height: 26px;
  line-height: 26px;
  user-select: none;
}

.el-tag:hover {
  opacity: 0.85;
}

.el-tag.active {
  background-color: var(--el-color-primary);
  border-color: var(--el-color-primary);
  color: #fff;
}

:deep(.el-scrollbar__wrap) {
  display: flex;
  align-items: center;
}

:deep(.el-tag .el-tag__close) {
  right: -4px;
  color: inherit;
  font-size: 12px;
}

:deep(.el-tag .el-tag__close:hover) {
  background-color: transparent;
  color: inherit;
  opacity: 0.8;
}
</style> 