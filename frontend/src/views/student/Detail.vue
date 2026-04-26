<template>
  <div class="student-detail">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item :to="{ path: '/students' }">学生管理</el-breadcrumb-item>
      <el-breadcrumb-item>详情</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card v-loading="loading">
      <template #header>
        <span>学生信息</span>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="学号">{{ student.student_no }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ student.name }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ student.gender }}</el-descriptions-item>
        <el-descriptions-item label="年龄">{{ student.age }}</el-descriptions-item>
        <el-descriptions-item label="班级">{{ student.class_no }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ student.phone }}</el-descriptions-item>
        <el-descriptions-item label="籍贯">{{ student.birth_place }}</el-descriptions-item>
        <el-descriptions-item label="毕业院校">{{ student.graduate_school }}</el-descriptions-item>
        <el-descriptions-item label="专业">{{ student.major }}</el-descriptions-item>
        <el-descriptions-item label="学历">{{ student.education }}</el-descriptions-item>
        <el-descriptions-item label="入学时间">{{ student.entrance_time }}</el-descriptions-item>
        <el-descriptions-item label="毕业时间">{{ student.graduate_time }}</el-descriptions-item>
        <el-descriptions-item label="顾问">{{ student.advisor_name }}</el-descriptions-item>
        <el-descriptions-item label="身份证">{{ student.id_card }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStudent } from '@/api/student'
import type { Student } from '@/types/student'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const student = ref<Student>({} as Student)

async function loadData() {
  loading.value = true
  try {
    const studentNo = route.params.studentNo as string
    const res = await getStudent(studentNo)
    student.value = res.data as Student
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.student-detail {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>