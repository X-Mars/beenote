<template>
  <div class="notes-container">
    <div class="header">
      <div class="left">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>新建笔记
        </el-button>
        <el-select 
          v-model="currentGroup" 
          placeholder="选择分组" 
          clearable
          class="group-select"
        >
          <el-option
            v-for="group in groups"
            :key="group.id"
            :label="group.name"
            :value="group.id"
          >
            <el-icon><FolderOpened /></el-icon>
            <span>{{ group.name }}</span>
          </el-option>
        </el-select>
      </div>
      <div class="right">
        <el-input
          v-model="searchKey"
          placeholder="搜索笔记"
          class="search-input"
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-radio-group v-model="viewMode" size="small">
          <el-radio-button label="table">
            <el-icon><List /></el-icon>
          </el-radio-button>
          <el-radio-button label="grid">
            <el-icon><Grid /></el-icon>
          </el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <template v-if="viewMode === 'table'">
      <el-table 
        :data="filteredNotes" 
        v-loading="loading"
        :row-class-name="tableRowClassName"
        stripe
      >
        <el-table-column prop="title" label="标题">
          <template #default="{ row }">
            <div class="note-title clickable" @click="navigateToView(row)">
              <el-icon><Document /></el-icon>
              <span>{{ row.title }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="group_id" label="分组">
          <template #default="{ row }">
            <el-tag size="small">
              {{ row.group_detail?.name || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
        <el-table-column label="操作" :width="showAuthButton ? 280 : 200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button 
                type="primary" 
                :icon="Edit"
                @click="navigateToEdit(row)"
              >
                编辑
              </el-button>
              <el-button 
                v-if="showAuthButton"
                type="success" 
                :icon="Key"
                @click="handleAuth(row)"
              >
                授权
              </el-button>
              <el-button 
                type="danger" 
                :icon="Delete"
                @click="handleDelete(row)"
              >
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </template>

    <template v-else>
      <el-row :gutter="20">
        <el-col 
          :span="6" 
          v-for="note in filteredNotes" 
          :key="note.id"
        >
          <el-card 
            class="note-card" 
            :body-style="{ padding: '15px' }"
            shadow="hover"
            @click="navigateToView(note)"
          >
            <div class="note-card-header">
              <span class="title">{{ note.title }}</span>
              <div class="header-right">
                <el-tag 
                  size="small" 
                  type="warning" 
                  effect="plain"
                  class="creator-tag"
                >
                  {{ note.creator?.name || note.creator?.username }}
                </el-tag>
                <el-dropdown trigger="click">
                  <el-button type="text" @click.stop>
                    <el-icon><More /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click.stop="navigateToEdit(note)">
                        <el-icon><Edit /></el-icon>编辑
                      </el-dropdown-item>
                      <el-dropdown-item 
                        v-if="showAuthButton"
                        @click.stop="handleAuth(note)"
                      >
                        <el-icon><Key /></el-icon>授权
                      </el-dropdown-item>
                      <el-dropdown-item 
                        @click.stop="handleDelete(note)"
                        class="danger"
                      >
                        <el-icon><Delete /></el-icon>删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
            <div class="note-card-content">
              <MdPreview :modelValue="note.content.slice(0, 100) || ''" />
            </div>
            <div class="note-card-footer">
              <el-tag size="small">
                {{ note.group_detail?.name || '-' }}
              </el-tag>
              <span class="time">
                {{ formatTime(note.updated_at) }}
              </span>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </template>

    <el-dialog
      v-model="authDialogVisible"
      title="笔记授权"
      width="600px"
    >
      <el-table
        :data="users"
        v-loading="usersLoading"
        style="width: 100%"
      >
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column label="授权" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.hasAuth"
              @change="handleAuthChange(row)"
            />
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Plus,
  Edit,
  Delete,
  Search,
  List,
  Grid,
  Document,
  FolderOpened,
  More,
  Key
} from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { 
  getNotes, 
  getGroups, 
  deleteNote, 
  getUsers,
  updateUser
} from '@/api'
import type { Note, Group } from '@/api/types'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { debounce } from 'lodash-es'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { useUserStore } from '@/store/user'

dayjs.extend(relativeTime)

const router = useRouter()
const notes = ref<Note[]>([])
const groups = ref<Group[]>([])
const loading = ref(false)
const currentGroup = ref<number | null>(null)
const searchKey = ref('')
const viewMode = ref<'table' | 'grid'>('grid')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const filteredNotes = computed(() => notes.value)

const formatTime = (time: string) => {
  return dayjs(time).fromNow()
}

const tableRowClassName = ({ row }: { row: Note }) => {
  const now = dayjs()
  const updated = dayjs(row.updated_at)
  if (now.diff(updated, 'day') < 1) {
    return 'recent-row'
  }
  return ''
}

const fetchNotes = async () => {
  loading.value = true
  try {
    const res = await getNotes({
      page: currentPage.value,
      page_size: pageSize.value,
      group__id: currentGroup.value || undefined
    })
    notes.value = res.data.results
    total.value = res.data.count
  } catch (error) {
    console.error(error)
    ElMessage.error('获取笔记列表失败')
  } finally {
    loading.value = false
  }
}

const fetchGroups = async () => {
  try {
    const res = await getGroups()
    groups.value = res.data
  } catch (error) {
    console.error(error)
  }
}

const handleAdd = () => {
  router.push('/notes/edit')
}

const navigateToEdit = (note: Note) => {
  router.push(`/notes/edit/${note.id}`)
}

const handleDelete = async (note: Note) => {
  try {
    await ElMessageBox.confirm('确定要删除该笔记吗？', '提示', {
      type: 'warning'
    })
    await deleteNote(note.id)
    await fetchNotes()
  } catch (error) {
    console.error(error)
  }
}

const handleSearch = debounce(() => {
  fetchNotes()
}, 300)

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  fetchNotes()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchNotes()
}

const navigateToView = (note: Note) => {
  router.push(`/notes/view/${note.id}`)
}

watch([currentGroup, searchKey], () => {
  currentPage.value = 1
  fetchNotes()
})

const authDialogVisible = ref(false)
const users = ref([])
const usersLoading = ref(false)
const currentNote = ref(null)

const handleAuth = async (note: Note) => {
  currentNote.value = note
  authDialogVisible.value = true
  await fetchUsers()
}

const fetchUsers = async () => {
  if (!currentNote.value) return
  usersLoading.value = true
  try {
    const res = await getUsers()
    users.value = res.data.map(user => ({
      ...user,
      hasAuth: user.notes?.includes(currentNote.value.id)
    }))
  } catch (error) {
    console.error(error)
  } finally {
    usersLoading.value = false
  }
}

const handleAuthChange = async (user: any) => {
  if (!currentNote.value) return
  try {
    const noteIds = user.hasAuth
      ? [...(user.notes || []), currentNote.value.id]
      : (user.notes || []).filter(id => id !== currentNote.value.id)
    
    await updateUser(user.id, {
      note: noteIds,
      note_group: user.note_group || []
    })
    
    user.notes = noteIds
    ElMessage.success('授权更新成功')
  } catch (error: any) {
    console.error(error)
    ElMessage.error(error.response?.data?.detail || '授权更新失败')
    user.hasAuth = !user.hasAuth
  }
}

const userStore = useUserStore()

const showAuthButton = computed(() => userStore.user?.role === 'admin')

onMounted(() => {
  fetchNotes()
  fetchGroups()
})
</script>

<style scoped>
.notes-container {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left, .right {
  display: flex;
  gap: 15px;
  align-items: center;
}

.group-select {
  width: 200px;
}

.search-input {
  width: 300px;
}

.note-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.recent-row) {
  background-color: var(--el-color-primary-light-9);
}

.note-card {
  margin-bottom: 20px;
  transition: all 0.3s;
  border: 1px solid #e4e7ed;
}

.note-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  border-color: var(--el-color-primary-light-7);
}

.note-card :deep(.el-card__body) {
  padding: 15px;
  border-radius: 4px;
}

.note-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.note-card-header .title {
  font-weight: bold;
  font-size: 16px;
}

.note-card-content {
  color: var(--el-text-color-regular);
  margin-bottom: 15px;
  height: 150px;
  overflow: hidden;
}

.note-card-content :deep(.md-preview) {
  background-color: transparent;
  padding: 0;
  font-size: 13px;
}

.note-card-content :deep(.md-preview img) {
  max-height: 100px;
}

.note-card-content :deep(.md-preview h1) {
  font-size: 16px;
}

.note-card-content :deep(.md-preview h2) {
  font-size: 15px;
}

.note-card-content :deep(.md-preview h3,
.md-preview h4,
.md-preview h5,
.md-preview h6) {
  font-size: 14px;
}

.note-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.note-card-footer .time {
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

:deep(.danger) {
  color: var(--el-color-danger);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.clickable {
  cursor: pointer;
}

.clickable:hover {
  color: var(--el-color-primary);
}

.note-card {
  cursor: pointer;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.creator-tag {
  font-size: 12px;
}
</style> 