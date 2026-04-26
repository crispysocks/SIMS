<template>
  <div class="classes-form">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item :to="{ path: '/classes' }">班级管理</el-breadcrumb-item>
      <el-breadcrumb-item>{{ isEdit ? '编辑' : '新增' }}</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card v-loading="loading">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="班级编号" prop="class_no">
              <el-input v-model="form.class_no" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="班级名称" prop="class_name">
              <el-input v-model="form.class_name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="开课时间" prop="class_open_time">
              <el-date-picker v-model="form.class_open_time" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="班主任" prop="head_teacher_no">
              <el-input v-model="form.head_teacher_no" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="授课老师" prop="instructor_no">
              <el-input v-model="form.instructor_no" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="描述" prop="description">
              <el-input v-model="form.description" type="textarea" :rows="3" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { getClass, createClass, updateClass } from '@/api/classes'
import type { ClassInfoCreate } from '@/types/classes'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const classNo = route.params.classNo as string
const isEdit = computed(() => !!classNo)

const form = reactive<ClassInfoCreate>({
  class_no: '',
  class_name: '',
  class_open_time: '',
  head_teacher_no: '',
  instructor_no: '',
  description: ''
})

const rules: FormRules = {
  class_no: [{ required: true, message: '请输入班级编号', trigger: 'blur' }],
  class_name: [{ required: true, message: '请输入班级名称', trigger: 'blur' }],
  class_open_time: [{ required: true, message: '请选择开课时间', trigger: 'change' }]
}

async function loadData() {
  if (!classNo) return
  loading.value = true
  try {
    const res = await getClass(classNo)
    Object.assign(form, res.data)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    if (isEdit.value) {
      await updateClass(classNo, form as any)
      ElMessage.success('更新成功')
    } else {
      await createClass(form)
      ElMessage.success('创建成功')
    }
    router.push('/classes')
  } catch (e) {
    console.error(e)
  }
}

function handleCancel() {
  router.back()
}

onMounted(() => {
  if (classNo) {
    loadData()
  }
})
</script>

<style scoped lang="scss">
.classes-form {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>