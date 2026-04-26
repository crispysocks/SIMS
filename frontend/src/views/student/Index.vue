<template>
  <div class="student-index">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>学生管理</el-breadcrumb-item>
    </el-breadcrumb>

    <search-form :fields="searchFields" @search="handleSearch" class="mt-4" />

    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增学生</el-button>
      <el-button @click="handleBatchDelete" :disabled="selectedRows.length === 0">批量删除</el-button>
      <el-button @click="handleRestore" :disabled="selectedRows.length === 0">批量恢复</el-button>
    </div>

    <data-table
      :data="tableData"
      :columns="columns"
      :loading="loading"
      :total="total"
      :show-selection="true"
      :show-action="true"
      show-pagination
      @selection-change="handleSelectionChange"
      @page-change="handlePageChange"
    >
      <template #action="{ row }">
        <el-button link type="primary" @click="handleView(row)">查看</el-button>
        <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
        <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
      </template>
    </data-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import SearchForm from '@/components/SearchForm.vue'
import DataTable from '@/components/DataTable.vue'
import { getStudents, deleteStudents, restoreStudents } from '@/api/student'
import type { Student } from '@/types/student'

const router = useRouter()
const loading = ref(false)
const tableData = ref<Student[]>([])
const total = ref(0)
const selectedRows = ref<Student[]>([])
const searchData = ref<Record<string, unknown>>({})

const searchFields = [
  { prop: 'name', label: '姓名', type: 'input', placeholder: '请输入姓名' }
]

const columns = [
  { prop: 'student_no', label: '学号', width: '120' },
  { prop: 'name', label: '姓名', width: '100' },
  { prop: 'gender', label: '性别', width: '60' },
  { prop: 'age', label: '年龄', width: '60' },
  { prop: 'class_no', label: '班级', width: '100' },
  { prop: 'phone', label: '电话', width: '130' }
]

async function loadData() {
  loading.value = true
  try {
    const res = await getStudents({ ...searchData.value, page: 1, page_size: 20 })
    tableData.value = res.data.items || []
    total.value = res.data.total || 0
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

function handleSelectionChange(rows: Record<string, unknown>[]) {
  selectedRows.value = rows as Student[]
}

function handlePageChange(page: number, pageSize: number) {
  loadData()
}

function handleAdd() {
  router.push('/students/form')
}

function handleEdit(row: Student) {
  router.push(`/students/form/${row.student_no}`)
}

function handleView(row: Student) {
  router.push(`/students/${row.student_no}`)
}

async function handleDelete(row: Student) {
  try {
    await ElMessageBox.confirm('确定要删除该学生吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteStudents([row.student_no])
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    // cancelled
  }
}

async function handleBatchDelete() {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 个学生吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteStudents(selectedRows.value.map(r => r.student_no))
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    // cancelled
  }
}

async function handleRestore() {
  try {
    await restoreStudents(selectedRows.value.map(r => r.student_no))
    ElMessage.success('恢复成功')
    loadData()
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.student-index {
  padding: 20px;
}

.mt-4 {
  margin-top: 16px;
}

.toolbar {
  margin-bottom: 16px;
  display: flex;
  gap: 8px;
}
</style>