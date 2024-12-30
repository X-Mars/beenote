<template>
  <div class="auth-groups-container">
    <div class="header">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>新建分组
      </el-button>
    </div>

    <el-table 
      :data="groups" 
      v-loading="loading"
      stripe
    >
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="description" label="描述" />
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
import { ref, onMounted } from 'vue'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
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

const rules: FormRules = {
  name: [{ required: true, message: '请输入分组名称', trigger: 'blur' }]
}

const fetchGroups = async () => {
  loading.value = true
  try {
    const res = await getGroups()
    groups.value = res.data
  } catch (error) {
    console.error(error)
    ElMessage.error('获取分组列表失败')
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
        console.error(error)
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
      '确定要删除该分组吗？此操作不可恢复',
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
      console.error(error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchGroups()
})
</script>

<style scoped>
.auth-groups-container {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}
</style>
