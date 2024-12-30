<template>
  <div class="users-container">
    <div class="header">
      <el-button type="primary" @click="handleAdd">
        <el-icon><Plus /></el-icon>新建用户
      </el-button>
    </div>

    <el-table 
      :data="users" 
      v-loading="loading"
      stripe
    >
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="first_name" label="姓" />
      <el-table-column prop="last_name" label="名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="role" label="角色">
        <template #default="{ row }">
          <el-tag>{{ row.role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_active_at" label="最后活跃时间" />
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
      :title="currentUser ? '编辑用户' : '新建用户'"
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
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item 
          label="密码" 
          prop="password"
          :rules="currentUser ? [] : [{ required: true, message: '请输入密码' }]"
        >
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        <el-form-item label="姓" prop="first_name">
          <el-input v-model="form.first_name" />
        </el-form-item>
        <el-form-item label="名" prop="last_name">
          <el-input v-model="form.last_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="form.is_active" />
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
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { getUsers, createUser, updateUser, deleteUser } from '@/api'
import type { User } from '@/api/types'

const users = ref<User[]>([])
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const currentUser = ref<User | null>(null)
const formRef = ref<FormInstance>()

const form = reactive({
  username: '',
  password: '',
  first_name: '',
  last_name: '',
  email: '',
  role: 'user',
  is_active: true
})

const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  email: [{ type: 'email', message: '请输入正确的邮箱地址' }]
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getUsers()
    users.value = res.data
  } catch (error) {
    console.error(error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  form.username = ''
  form.password = ''
  form.first_name = ''
  form.last_name = ''
  form.email = ''
  form.role = 'user'
  form.is_active = true
  currentUser.value = null
}

const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (user: User) => {
  currentUser.value = user
  form.username = user.username
  form.password = ''
  form.first_name = user.first_name
  form.last_name = user.last_name
  form.email = user.email
  form.role = user.role
  form.is_active = user.is_active
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const data = { ...form }
        if (currentUser.value) {
          if (!data.password) {
            delete data.password
          }
          await updateUser(currentUser.value.id, data)
        } else {
          await createUser(data)
        }
        ElMessage.success('保存成功')
        dialogVisible.value = false
        fetchUsers()
      } catch (error) {
        console.error(error)
        ElMessage.error('保存失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleDelete = async (user: User) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该用户吗？此操作不可恢复',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteUser(user.id)
    ElMessage.success('删除成功')
    await fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error(error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users-container {
  padding: 20px;
}

.header {
  margin-bottom: 20px;
}
</style> 