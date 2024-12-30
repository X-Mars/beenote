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
            <div class="note-title">
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
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button 
                type="primary" 
                :icon="Edit"
                @click="handleEdit(row)"
              >
                编辑
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
          >
            <div class="note-card-header">
              <span class="title">{{ note.title }}</span>
              <el-dropdown trigger="click">
                <el-button type="text">
                  <el-icon><More /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleEdit(note)">
                      <el-icon><Edit /></el-icon>编辑
                    </el-dropdown-item>
                    <el-dropdown-item 
                      @click="handleDelete(note)"
                      class="danger"
                    >
                      <el-icon><Delete /></el-icon>删除
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            <div class="note-card-content">
              {{ note.content.slice(0, 100) }}...
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

    <note-dialog
      v-model="dialogVisible"
      :note="currentNote"
      :groups="groups"
      @success="fetchNotes"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { 
  Plus,
  Edit,
  Delete,
  Search,
  List,
  Grid,
  Document,
  FolderOpened,
  More
} from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'
import { getNotes, getGroups, deleteNote } from '@/api'
import type { Note, Group } from '@/api/types'
import NoteDialog from '@/components/NoteDialog.vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { debounce } from 'lodash-es'

dayjs.extend(relativeTime)

const notes = ref<Note[]>([])
const groups = ref<Group[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const currentNote = ref<Partial<Note> | null>(null)
const currentGroup = ref<number | null>(null)
const searchKey = ref('')
const viewMode = ref<'table' | 'grid'>('table')
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
    const params: Record<string, any> = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    if (currentGroup.value) {
      params.group__id = currentGroup.value
    }
    
    if (searchKey.value) {
      params.search = searchKey.value
    }
    
    const res = await getNotes(params)
    notes.value = res.data.results
    total.value = res.data.count
  } catch (error) {
    console.error(error)
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
  currentNote.value = null
  dialogVisible.value = true
}

const handleEdit = (note: Note) => {
  currentNote.value = { ...note }
  console.log('currentNote:', currentNote.value)
  // 请删除currentNote中的created_at和updated_at
  delete currentNote.value.created_at
  delete currentNote.value.updated_at
  dialogVisible.value = true
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

watch([currentGroup, searchKey], () => {
  currentPage.value = 1
  fetchNotes()
})

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
}

.note-card:hover {
  transform: translateY(-5px);
}

.note-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.note-card-header .title {
  font-weight: bold;
  font-size: 16px;
}

.note-card-content {
  color: var(--el-text-color-regular);
  margin-bottom: 15px;
  height: 60px;
  overflow: hidden;
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
</style> 