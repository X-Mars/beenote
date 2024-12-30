<template>
  <el-dialog
    :title="props.note ? '编辑笔记' : '新建笔记'"
    v-model="dialogVisible"
    width="800px"
  >
    <el-form
      :model="form"
      :rules="rules"
      ref="formRef"
      label-width="80px"
    >
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" />
      </el-form-item>
      <el-form-item label="分组" prop="group">
        <el-select v-model="form.group" placeholder="选择分组">
          <el-option
            v-for="group in props.groups"
            :key="group.id"
            :label="group.name"
            :value="group.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="内容" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="10"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { createNote, updateNote } from '@/api'
import type { Note, Group } from '@/api/types'
import type { FormInstance } from 'element-plus'

const props = defineProps<{
  modelValue: boolean
  note: Partial<Note> | null
  groups: Group[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'success'): void
}>()

const formRef = ref<FormInstance>()
const submitting = ref(false)

const form = reactive({
  title: '',
  content: '',
  group: undefined as number | undefined
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  group: [{ required: true, message: '请选择分组', trigger: 'change' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

watch(() => props.note, (newVal) => {
  if (newVal) {
    form.title = newVal.title
    form.content = newVal.content
    form.group = newVal.group
  } else {
    form.title = ''
    form.content = ''
    form.group = undefined
  }
}, { immediate: true })

const handleClose = () => {
  dialogVisible.value = false
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (props.note?.id) {
          await updateNote(props.note.id, form)
        } else {
          await createNote(form)
        }
        ElMessage.success('保存成功')
        dialogVisible.value = false
        emit('success')
      } catch (error) {
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}
</script> 