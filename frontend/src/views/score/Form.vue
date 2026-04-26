<template>
  <div class="score-form">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item :to="{ path: '/scores' }">成绩管理</el-breadcrumb-item>
      <el-breadcrumb-item>{{ isEdit ? '编辑' : '录入' }}成绩</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学生" prop="student_no">
              <el-select v-model="form.student_no" placeholder="请选择学生" filterable>
                <el-option v-for="s in students" :key="s.student_no" :label="s.name" :value="s.student_no" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="考试名称" prop="exam_name">
              <el-input v-model="form.exam_name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="考试序次" prop="exam_no">
              <el-input-number v-model="form.exam_no" :min="1" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="成绩" prop="score">
              <el-input-number v-model="form.score" :min="0" :max="100" :precision="1" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="考试日期" prop="exam_date">
              <el-date-picker v-model="form.exam_date" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="form.remark" type="textarea" :rows="2" />
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
import { getScores, createScore, updateScore } from '@/api/score'
import { getStudents } from '@/api/student'
import type { ScoreCreate } from '@/types/score'
import type { Student } from '@/types/student'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const students = ref<Student[]>([])

const form = reactive<ScoreCreate>({
  student_no: '',
  exam_no: 1,
  exam_name: '',
  score: 0,
  exam_date: '',
  remark: ''
})

const rules: FormRules = {
  student_no: [{ required: true, message: '请选择学生', trigger: 'change' }],
  exam_name: [{ required: true, message: '请输入考试名称', trigger: 'blur' }],
  exam_no: [{ required: true, message: '请输入考试序次', trigger: 'blur' }],
  score: [{ required: true, message: '请输入成绩', trigger: 'blur' }]
}

async function loadStudents() {
  try {
    const res = await getStudents()
    students.value = res.data.items || []
  } catch (e) {
    console.error(e)
  }
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    await createScore(form)
    ElMessage.success('提交成功')
    router.push('/scores')
  } catch (e) {
    console.error(e)
  }
}

function handleCancel() {
  router.back()
}

onMounted(() => {
  loadStudents()
})
</script>

<style scoped lang="scss">
.score-form {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>