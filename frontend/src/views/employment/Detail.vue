<template>
  <div class="employment-detail">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item :to="{ path: '/employment' }">就业管理</el-breadcrumb-item>
      <el-breadcrumb-item>详情</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card v-loading="loading">
      <template #header>
        <span>就业信息</span>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="学号">{{ employment.student_no }}</el-descriptions-item>
        <el-descriptions-item label="公司">{{ employment.company }}</el-descriptions-item>
        <el-descriptions-item label="薪资">{{ employment.salary }}</el-descriptions-item>
        <el-descriptions-item label="就业状态">{{ employment.status }}</el-descriptions-item>
        <el-descriptions-item label="开放时间">{{ employment.open_time }}</el-descriptions-item>
        <el-descriptions-item label="签约时间">{{ employment.offer_time }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { v2GetEmployment } from '@/api/employment'
import type { Employment } from '@/types/employment'

const route = useRoute()
const loading = ref(false)
const employment = ref<Employment>({} as Employment)

async function loadData() {
  loading.value = true
  try {
    const studentNo = route.params.studentNo as string
    const res = await v2GetEmployment(studentNo)
    employment.value = res.data as Employment
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
.employment-detail {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>