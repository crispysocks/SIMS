<template>
  <div class="teacher-form">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item :to="{ path: '/teachers' }">教师管理</el-breadcrumb-item>
      <el-breadcrumb-item>{{ isEdit ? '编辑' : '新增' }}</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card v-loading="loading">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="教师编号" prop="teacher_no">
              <el-input v-model="form.teacher_no" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电话" prop="phone">
              <el-input v-model="form.phone" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="授课科目" prop="subject">
              <el-input v-model="form.subject" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身份证" prop="id_card">
              <el-input v-model="form.id_card" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="出生日期" prop="birthday">
              <el-date-picker v-model="form.birthday" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="入职日期" prop="hire_date">
              <el-date-picker v-model="form.hire_date" type="date" style="width: 100%" />
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
import { getTeacher, createTeacher, updateTeacher } from '@/api/teacher'
import type { TeacherCreate } from '@/types/teacher'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const teacherNo = route.params.teacherNo as string
const isEdit = computed(() => !!teacherNo)

const form = reactive<TeacherCreate>({
  teacher_no: '',
  name: '',
  gender: '男',
  phone: '',
  email: '',
  subject: '',
  id_card: '',
  birthday: '',
  hire_date: ''
})

const rules: FormRules = {
  teacher_no: [{ required: true, message: '请输入教师编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
}

async function loadData() {
  if (!teacherNo) return
  loading.value = true
  try {
    const res = await getTeacher(teacherNo)
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
      await updateTeacher(teacherNo, form as any)
      ElMessage.success('更新成功')
    } else {
      await createTeacher(form)
      ElMessage.success('创建成功')
    }
    router.push('/teachers')
  } catch (e) {
    console.error(e)
  }
}

function handleCancel() {
  router.back()
}

onMounted(() => {
  if (teacherNo) {
    loadData()
  }
})
</script>

<style scoped lang="scss">
.teacher-form {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>