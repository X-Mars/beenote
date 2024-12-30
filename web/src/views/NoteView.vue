<template>
  <div class="note-view-container">
    <div class="header">
      <div class="title-row">
        <h1 class="title">{{ note.title }}</h1>
        <el-button type="primary" @click="handleEdit">编辑文章</el-button>
      </div>
      <div class="meta">
        <el-tag size="small" v-if="note.group_detail">
          {{ note.group_detail.name }}
        </el-tag>
        <span class="time">更新于 {{ formatTime(note.updated_at || '') }}</span>
      </div>
    </div>
    <div class="content">
      <MdPreview :modelValue="note.content || ''" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { getNote } from '@/api'
import type { Note } from '@/api/types'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const note = ref<Partial<Note>>({})

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

const fetchNote = async (id: number) => {
  try {
    const res = await getNote(id)
    note.value = res.data
  } catch (error) {
    console.error(error)
    ElMessage.error('获取笔记失败')
  }
}

const handleEdit = () => {
  router.push(`/notes/edit/${route.params.id}`)
}

onMounted(() => {
  if (route.params.id) {
    fetchNote(Number(route.params.id))
  }
})
</script>

<style scoped>
.note-view-container {
  padding: 10px;
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #dcdfe6;
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.title {
  margin: 0;
  font-size: 28px;
  color: var(--el-text-color-primary);
}

.meta {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 0;
  color: var(--el-text-color-secondary);
}

.time {
  font-size: 14px;
}

.content {
  background-color: #fff;
  border-radius: 4px;
  /* padding: 0px; */
}

:deep(.md-editor) {
  border: none;
}

:deep(.md-preview) {
  background-color: #fff;
  padding: 0;
}
</style> 