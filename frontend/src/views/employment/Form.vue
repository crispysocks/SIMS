<template>
  <div class="employment-form">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item :to="{ path: '/employment' }">就业管理</el-breadcrumb-item>
      <el-breadcrumb-item>{{ isEdit ? '编辑' : '新增' }}就业信息</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card v-loading="loading">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学生" prop="student_no">
              <el-select v-model="form.student_no" placeholder="请选择学生" filterable :disabled="isEdit">
                <el-option v-for="s in students" :key="s.student_no" :label="s.name" :value="s.student_no" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="公司" prop="company">
              <el-input v-model="form.company" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="薪资" prop="salary">
              <el-input-number v-model="form.salary" :min="0" :step="1000" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择状态">
                <el-option label="待业" value="待业" />
                <el-option label="在聘" value="在聘" />
                <el-option label="已离职" value="已离职" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="开放时间" prop="open_time">
              <el-date-picker v-model="form.open_time" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="签约时间" prop="offer_time">
              <el-date-picker v-model="form.offer_time" type="date" style="width: 100%" />
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
import { v2GetEmployment, v2CreateEmployment, v2UpdateEmployment } from '@/api/employment'
import { getStudents } from '@/api/student'
import type { EmploymentCreate, EmploymentUpdate } from '@/types/employment'
import type { Student } from '@/types/student'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const students = ref<Student[]>([])
const studentNo = route.params.studentNo as string
const isEdit = computed(() => !!studentNo)

const form = reactive<EmploymentCreate & EmploymentUpdate>({
  student_no: '',
  company: '',
  salary: 0,
  status: '待业',
  open_time: '',
  offer_time: ''
})

const rules: FormRules = {
  student_no: [{ required: true, message: '请选择学生', trigger: 'change' }],
  company: [{ required: true, message: '请输入公司', trigger: 'blur' }],
  salary: [{ required: true, message: '请输入薪资', trigger: 'blur' }]
}

async function loadStudents() {
  try {
    const res = await getStudents()
    students.value = res.data.items || []
  } catch (e) {
    console.error(e)
  }
}

async function loadData() {
  if (!studentNo) return
  loading.value = true
  try {
    const res = await v2GetEmployment(studentNo)
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
      await v2UpdateEmployment(studentNo, form)
      ElMessage.success('更新成功')
    } else {
      await v2CreateEmployment(form as EmploymentCreate)
      ElMessage.success('创建成功')
    }
    router.push('/employment')
  } catch (e) {
    console.error(e)
  }
}

function handleCancel() {
  router.back()
}

onMounted(() => {
  loadStudents()
  if (studentNo) {
    loadData()
  }
})
</script>

<style scoped lang="scss">
.employment-form {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>