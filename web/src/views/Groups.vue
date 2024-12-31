<template>
  <div class="groups-container">
    <div class="header">
      <div class="left">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>新建分组
        </el-button>
      </div>
      <div class="right">
        <el-input
          v-model="searchKey"
          placeholder="搜索分组"
          class="search-input"
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-radio-group v-model="viewMode" size="small">
          <el-radio-button value="table">
            <el-icon><List /></el-icon>
          </el-radio-button>
          <el-radio-button value="grid">
            <el-icon><Grid /></el-icon>
          </el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <!-- 表格视图 -->
    <template v-if="viewMode === 'table'">
      <el-table 
        :data="filteredGroups" 
        v-loading="loading"
        stripe
      >
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column 
          prop="note_count" 
          label="笔记数量" 
          width="120"
          align="center"
        >
          <template #default="{ row }">
            <el-button
              text
              style="color: #E6A23C;"
              @click="showNotes(row)"
            >
              {{ row.note_count }} 篇笔记
            </el-button>
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
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              <!-- 只有管理员可见的授权按钮 -->
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
    </template>

    <!-- 卡片视图 -->
    <template v-else>
      <el-row :gutter="20">
        <el-col 
          :span="6" 
          v-for="group in filteredGroups" 
          :key="group.id"
        >
          <el-card 
            class="group-card" 
            :body-style="{ padding: '15px' }"
            shadow="hover"
          >
            <div class="group-header">
              <span class="title">{{ group.name }}</span>
              <el-dropdown trigger="click">
                <el-button type="text">
                  <el-icon><More /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleEdit(group)">
                      <el-icon><Edit /></el-icon>编辑
                    </el-dropdown-item>
                    <el-dropdown-item 
                      v-if="showAuthButton"
                      @click="handleAuth(group)"
                    >
                      <el-icon><Key /></el-icon>授权
                    </el-dropdown-item>
                    <el-dropdown-item 
                      @click="handleDelete(group)"
                      class="danger"
                    >
                      <el-icon><Delete /></el-icon>删除
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            <div class="group-content">
              {{ group.description || '暂无描述' }}
            </div>
            <div class="group-footer">
              <el-button
                text
                style="color: #E6A23C;"
                @click="showNotes(group)"
              >
                {{ group.note_count }} 篇笔记
              </el-button>
              <span class="time">
                {{ formatTime(group.updated_at) }}
              </span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </template>

    <!-- 编辑对话框 -->
    <el-dialog
      :title="currentGroup ? '编辑分组' : '新建分组'"
      v-model="dialogVisible"
      width="500px"
      @close="resetForm"
    >
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分组名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入分组描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 授权对话框 -->
    <el-dialog
      v-model="authDialogVisible"
      title="分组授权"
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

    <!-- 笔记列表对话框 -->
    <el-dialog
      v-model="notesDialogVisible"
      :title="`${currentGroup?.name || ''} 的笔记列表`"
      width="800px"
    >
      <el-table
        :data="groupNotes"
        v-loading="notesLoading"
        style="width: 100%"
      >
        <el-table-column prop="title" label="笔记名称">
          <template #default="{ row }">
            <el-button
              text
              style="color: #E6A23C;"
              @click="navigateToNote(row)"
            >
              {{ row.title }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="创建人">
          <template #default="{ row }">
            {{ row.creator?.name || row.creator?.username }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { 
  Plus, 
  Edit, 
  Delete, 
  Key, 
  List, 
  Grid,
  More,
  Search 
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { getGroups, createGroup, updateGroup, deleteGroup, getUsers, updateUser, getNotes } from '@/api'
import type { Group, Note } from '@/api/types'
import { useUserStore } from '@/store/user'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { debounce } from 'lodash-es'
import { useRouter } from 'vue-router/dist/vue-router.esm-bundler'

dayjs.extend(relativeTime)

// 添加视图模式
const viewMode = ref<'table' | 'grid'>('grid')

// 添加时间格式化函数
const formatTime = (time: string) => {
  return dayjs(time).fromNow()
}

const groups = ref<Group[]>([])
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入分组名称', trigger: 'blur' }]
}

const fetchGroups = async () => {
  loading.value = true
  try {
    const res = await getGroups()
    console.log('获取到的分组数据:', res)  // 添加调试日志
    groups.value = res.data || []
  } catch (error) {
    console.error('获取分组失败:', error)
    ElMessage.error('获取分组失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  form.name = ''
  form.description = ''
}

const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (group: Group) => {
  currentGroup.value = group
  form.name = group.name
  form.description = group.description || ''
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (currentGroup.value) {
          await updateGroup(currentGroup.value.id, form)
        } else {
          await createGroup(form)
        }
        ElMessage.success('保存成功')
        dialogVisible.value = false
        fetchGroups()
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleDelete = async (group: Group) => {
  try {
    await ElMessageBox.confirm(
      '删除分组将同时删除该分组下的所有笔记，是否继续？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteGroup(group.id)
    ElMessage.success('删除成功')
    await fetchGroups()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 授权相关
const authDialogVisible = ref(false)
const users = ref([])
const usersLoading = ref(false)
const currentAuthGroup = ref<Group | null>(null)

const userStore = useUserStore()
const showAuthButton = computed(() => userStore.user?.role === 'admin')

const handleAuth = async (group: Group) => {
  currentAuthGroup.value = group
  authDialogVisible.value = true
  await fetchUsers()
}

const fetchUsers = async () => {
  if (!currentAuthGroup.value) return
  usersLoading.value = true
  try {
    // 获取用户列表，包含 note_group 字段
    const res = await getUsers()
    users.value = res.data.map(user => ({
      ...user,
      // 根据用户的 note_group 字段判断是否有权限
      hasAuth: Array.isArray(user.note_group) && user.note_group.includes(currentAuthGroup.value.id)
    }))
  } catch (error) {
    console.error(error)
    ElMessage.error('获取用户列表失败')
  } finally {
    usersLoading.value = false
  }
}

const handleAuthChange = async (user: any) => {
  if (!currentAuthGroup.value) return
  try {
    // 确保 note_group 是数组
    const currentGroups = Array.isArray(user.note_group) ? [...user.note_group] : []
    
    if (user.hasAuth) {
      // 如果授权，将当前分组ID添加到列表中
      if (!currentGroups.includes(currentAuthGroup.value.id)) {
        currentGroups.push(currentAuthGroup.value.id)
      }
    } else {
      // 如果取消授权，从列表中移除当前分组ID
      const index = currentGroups.indexOf(currentAuthGroup.value.id)
      if (index > -1) {
        currentGroups.splice(index, 1)
      }
    }
    
    // 发送更新请求，同时保留 note 字段
    await updateUser(user.id, {
      note_group: currentGroups,
      note: user.notes || []  // 保留原有的笔记授权
    })
    
    // 更新本地状态
    user.note_group = currentGroups
    ElMessage.success('授权更新成功')
  } catch (error: any) {
    console.error(error)
    ElMessage.error(error.response?.data?.detail || '授权更新失败')
    user.hasAuth = !user.hasAuth
  }
}

// 添加搜索相关
const searchKey = ref('')

// 修改为过滤后的分组列表
const filteredGroups = computed(() => {
  if (!searchKey.value) return groups.value
  
  const key = searchKey.value.toLowerCase()
  return groups.value.filter(group => 
    group.name.toLowerCase().includes(key) || 
    (group.description && group.description.toLowerCase().includes(key))
  )
})

// 添加搜索防抖
const handleSearch = debounce(() => {
  // 如果后端支持搜索，可以在这里调用 fetchGroups
  // 目前使用前端过滤，所以这里暂时不需要实现
}, 300)

// 监听搜索关键字变化
watch(searchKey, () => {
  handleSearch()
})

// 笔记列表相关
const notesDialogVisible = ref(false)
const groupNotes = ref<Note[]>([])
const notesLoading = ref(false)
const currentGroup = ref<Group | null>(null)

const showNotes = async (group: Group) => {
  currentGroup.value = group
  notesDialogVisible.value = true
  await fetchGroupNotes(group.id)
}

const fetchGroupNotes = async (groupId: number) => {
  notesLoading.value = true
  try {
    const res = await getNotes({ group__id: groupId })
    groupNotes.value = res.data.results || []
  } catch (error) {
    console.error(error)
    ElMessage.error('获取笔记列表失败')
  } finally {
    notesLoading.value = false
  }
}

const router = useRouter()

// 添加笔记导航函数
const navigateToNote = (note: Note) => {
  notesDialogVisible.value = false
  router.push(`/notes/view/${note.id}`)
}

onMounted(() => {
  fetchGroups()
})
</script>

<style scoped>
.groups-container {
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

.group-card {
  margin-bottom: 20px;
  transition: all 0.3s;
  height: 100%;
}

.group-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  border-color: var(--el-color-primary-light-7);
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.group-header .title {
  font-weight: bold;
  font-size: 16px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.group-content {
  color: var(--el-text-color-regular);
  margin-bottom: 15px;
  min-height: 40px;
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.group-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.time {
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

:deep(.danger) {
  color: var(--el-color-danger);
}

:deep(.el-dropdown-menu__item i) {
  margin-right: 8px;
}

:deep(.el-card__body) {
  padding: 15px !important;
}

.search-input {
  width: 300px;
}

.left {
  display: flex;
  gap: 15px;
  align-items: center;
}

.group-footer .el-button {
  padding: 0;
  height: auto;
}
</style>
