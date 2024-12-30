<template>
  <div class="groups-container">
    <div class="header">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>新建分组
      </el-button>
    </div>

    <el-row :gutter="20" v-loading="loading">
      <el-col 
        :span="6" 
        v-for="group in groups" 
        :key="group.id"
      >
        <el-card 
          class="group-card" 
          :body-style="{ padding: '20px' }"
          shadow="hover"
        >
          <div class="group-header">
            <el-icon :size="24"><FolderOpened /></el-icon>
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
            <el-tag size="small" type="info">
              {{ group.note_count || 0 }} 篇笔记
            </el-tag>
            <el-tag size="small" type="success">
              {{ group.member_count || 0 }} 位成员
            </el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { Plus, Edit, Delete, More, FolderOpened } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { getGroups, createGroup, updateGroup, deleteGroup } from '@/api'
import type { Group } from '@/api/types'

const groups = ref<Group[]>([])
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const currentGroup = ref<Group | null>(null)
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
  currentGroup.value = null
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
}

.group-card {
  margin-bottom: 20px;
  transition: all 0.3s;
  height: 100%;
}

.group-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.group-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.group-header .title {
  flex: 1;
  font-size: 16px;
  font-weight: bold;
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
  gap: 10px;
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
</style> 