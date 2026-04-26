<template>
  <div class="student-form">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item :to="{ path: '/students' }">学生管理</el-breadcrumb-item>
      <el-breadcrumb-item>{{ isEdit ? '编辑' : '新增' }}</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card v-loading="loading">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学号" prop="student_no">
              <el-input v-model="form.student_no" :disabled="isEdit" />
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
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="form.age" :min="1" :max="99" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="班级" prop="class_no">
              <el-input v-model="form.class_no" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电话" prop="phone">
              <el-input v-model="form.phone" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="籍贯" prop="birth_place">
              <el-input v-model="form.birth_place" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毕业院校" prop="graduate_school">
              <el-input v-model="form.graduate_school" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="专业" prop="major">
              <el-input v-model="form.major" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学历" prop="education">
              <el-select v-model="form.education" placeholder="请选择">
                <el-option label="专科" value="专科" />
                <el-option label="本科" value="本科" />
                <el-option label="硕士" value="硕士" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="入学时间" prop="entrance_time">
              <el-date-picker v-model="form.entrance_time" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毕业时间" prop="graduate_time">
              <el-date-picker v-model="form.graduate_time" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="顾问" prop="advisor_name">
              <el-input v-model="form.advisor_name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身份证" prop="id_card">
              <el-input v-model="form.id_card" />
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
import { getStudent, createStudent, updateStudent } from '@/api/student'
import type { StudentCreate } from '@/types/student'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const studentNo = route.params.studentNo as string
const isEdit = computed(() => !!studentNo)

const form = reactive<StudentCreate>({
  student_no: '',
  class_no: '',
  name: '',
  gender: '男',
  age: 18,
  entrance_time: '',
  phone: '',
  birth_place: '',
  graduate_school: '',
  major: '',
  education: '本科',
  advisor_name: '',
  id_card: ''
})

const rules: FormRules = {
  student_no: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  class_no: [{ required: true, message: '请输入班级', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  entrance_time: [{ required: true, message: '请选择入学时间', trigger: 'change' }]
}

async function loadData() {
  if (!studentNo) return
  loading.value = true
  try {
    const res = await getStudent(studentNo)
    const data = res.data as StudentCreate
    Object.assign(form, data)
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
      await updateStudent(studentNo, form as any)
      ElMessage.success('更新成功')
    } else {
      await createStudent(form)
      ElMessage.success('创建成功')
    }
    router.push('/students')
  } catch (e) {
    console.error(e)
  }
}

function handleCancel() {
  router.back()
}

onMounted(() => {
  if (studentNo) {
    loadData()
  }
})
</script>

<style scoped lang="scss">
.student-form {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>