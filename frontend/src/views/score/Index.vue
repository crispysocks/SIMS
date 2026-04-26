<template>
  <div class="score-index">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>成绩管理</el-breadcrumb-item>
    </el-breadcrumb>

    <el-card>
      <search-form :fields="searchFields" @search="handleSearch" class="mb-4" />
      <div class="toolbar">
        <el-button type="primary" @click="handleAdd">录入成绩</el-button>
      </div>
      <data-table
        :data="tableData"
        :columns="columns"
        :loading="loading"
        :show-action="authStore.isAdmin || authStore.isTeacher"
      >
        <template #action="{ row }">
          <el-button v-if="authStore.isAdmin || authStore.isTeacher" link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button v-if="authStore.isAdmin" link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </data-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import SearchForm from '@/components/SearchForm.vue'
import DataTable from '@/components/DataTable.vue'
import { getScores, deleteScore as deleteScoreApi } from '@/api/score'
import { getStudents } from '@/api/student'
import { useAuthStore } from '@/stores/auth'
import type { Score } from '@/types/score'
import type { Student } from '@/types/student'

const authStore = useAuthStore()
const loading = ref(false)
const tableData = ref<Score[]>([])
const searchData = ref<Record<string, unknown>>({})
const students = ref<Student[]>([])

const searchFields = [
  {
    prop: 'student_no',
    label: '学生',
    type: 'select',
    placeholder: '请选择学生',
    options: [] as { label: string; value: string }[]
  }
]

const columns = [
  { prop: 'student_no', label: '学号', width: '120' },
  { prop: 'exam_no', label: '考试序次', width: '80' },
  { prop: 'exam_name', label: '考试名称', minWidth: '150' },
  { prop: 'score', label: '成绩', width: '80' },
  { prop: 'exam_date', label: '考试日期', width: '120' },
  { prop: 'remark', label: '备注', minWidth: '150' }
]

async function loadStudents() {
  try {
    const res = await getStudents()
    students.value = res.data.items || []
    searchFields[0].options = students.value.map(s => ({ label: s.name, value: s.student_no }))
  } catch (e) {
    console.error(e)
  }
}

async function loadData() {
  loading.value = true
  try {
    const studentNo = searchData.value.student_no as string
    if (studentNo) {
      const res = await getScores(studentNo)
      tableData.value = res.data as Score[] || []
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function handleSearch(data: Record<string, unknown>) {
  searchData.value = data
  loadData()
}

function handleAdd() {
  // Navigate to score form
}

function handleEdit(row: Score) {
  // Navigate to score edit
}

async function handleDelete(row: Score) {
  try {
    await ElMessageBox.confirm('确定要删除该成绩吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteScoreApi({
      student_no: row.student_no,
      exam_no: row.exam_no,
      exam_name: row.exam_name
    })
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    // cancelled
  }
}

onMounted(() => {
  loadStudents()
  if (students.value.length > 0) {
    searchData.value.student_no = students.value[0].student_no
    loadData()
  }
})
</script>

<style scoped lang="scss">
.score-index {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.toolbar {
  margin-bottom: 16px;
}
</style>