<template>
  <div class="note-edit-container">
    <div class="header">
      <div class="header-row">
        <el-input
          v-model="note.title"
          placeholder="请输入文章标题"
          class="title-input"
          :maxlength="100"
          show-word-limit
        />
        <el-select 
          v-model="note.group" 
          placeholder="选择分组"
          class="group-select"
        >
          <el-option
            v-for="group in groups"
            :key="group.id"
            :label="group.name"
            :value="group.id"
          />
        </el-select>
        <el-button type="primary" @click="handleSave" :loading="saving">
          {{ isEdit ? '保存文章' : '发布文章' }}
        </el-button>
      </div>
    </div>

    <div class="editor-container">
      <md-editor
        v-model="note.content"
        style="height: calc(100vh - 200px)"
        :preview="true"
        :toolbars="markdownToolbars"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { createNote, updateNote, getNote, getGroups } from '@/api'
import type { Note, Group } from '@/api/types'

const route = useRoute()
const router = useRouter()
const saving = ref(false)
const groups = ref<Group[]>([])
const isEdit = computed(() => !!route.params.id)

const note = ref<Partial<Note>>({
  title: '',
  content: '',
  group: null
})

// Markdown 工具栏配置
const markdownToolbars = [
  'bold', 'italic', 'strikethrough', 'heading', '|',
  'quote', 'code', 'link', '|',
  'list', 'ordered-list', 'check', '|',
  'preview', 'fullscreen'
]

// 获取笔记详情
const fetchNote = async (id: number) => {
  try {
    const res = await getNote(id)
    note.value = res.data
  } catch (error) {
    console.error(error)
    ElMessage.error('获取笔记失败')
  }
}

// 获取分组列表
const fetchGroups = async () => {
  try {
    const res = await getGroups()
    groups.value = res.data
  } catch (error) {
    console.error(error)
  }
}

// 保存笔记
const handleSave = async () => {
  if (!note.value.title?.trim()) {
    return ElMessage.warning('请输入标题')
  }

  if (!note.value.content?.trim()) {
    return ElMessage.warning('请输入内容')
  }

  saving.value = true
  try {
    let noteId: number
    if (route.params.id) {
      await updateNote(Number(route.params.id), note.value)
      noteId = Number(route.params.id)
      ElMessage.success('更新成功')
    } else {
      const res = await createNote(note.value)
      noteId = res.data.id
      ElMessage.success('创建成功')
    }
    router.push(`/notes/view/${noteId}`)
  } catch (error) {
    console.error(error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await fetchGroups()
  if (route.params.id) {
    await fetchNote(Number(route.params.id))
  }
})
</script>

<style scoped>
.note-edit-container {
  padding: 20px;
  height: 100%;
}

.header {
  margin-bottom: 20px;
}

.header-row {
  display: flex;
  align-items: center;
  gap: 15px;
}

.title-input {
  width: 500px;
}

.title-input :deep(.el-input__wrapper) {
  padding: 8px 15px;
}

.title-input :deep(.el-input__inner) {
  font-size: 20px;
  font-weight: bold;
  height: 100%;
  line-height: 34px;
}

.group-select {
  width: 200px;
}

/* .group-select :deep(.el-input__wrapper) {
  height: 50px;
} */

/* .group-select :deep(.el-input__inner) {
  height: 100%;
  line-height: 34px;
} */

:deep(.el-button) {
  padding: 0 20px;
  font-size: 16px;
}

.editor-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #fff;
}
</style> 