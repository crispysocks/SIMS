<template>
  <div class="teacher-index">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>教师管理</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增教师</el-button>
    </div>

    <data-table
      :data="tableData"
      :columns="columns"
      :loading="loading"
      :total="total"
      :show-action="true"
      show-pagination
      @page-change="handlePageChange"
    >
      <template #action="{ row }">
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
import DataTable from '@/components/DataTable.vue'
import { getTeachers, deleteTeacher } from '@/api/teacher'
import type { Teacher } from '@/types/teacher'

const router = useRouter()
const loading = ref(false)
const tableData = ref<Teacher[]>([])
const total = ref(0)

const columns = [
  { prop: 'teacher_no', label: '教师编号', width: '120' },
  { prop: 'name', label: '姓名', width: '100' },
  { prop: 'gender', label: '性别', width: '60' },
  { prop: 'phone', label: '电话', width: '130' },
  { prop: 'email', label: '邮箱', minWidth: '180' },
  { prop: 'subject', label: '授课科目', width: '100' }
]

async function loadData() {
  loading.value = true
  try {
    const res = await getTeachers()
    tableData.value = res.data as Teacher[] || []
    total.value = tableData.value.length
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function handlePageChange() {
  loadData()
}

function handleAdd() {
  router.push('/teachers/form')
}

function handleEdit(row: Teacher) {
  router.push(`/teachers/form/${row.teacher_no}`)
}

async function handleDelete(row: Teacher) {
  try {
    await ElMessageBox.confirm('确定要删除该教师吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteTeacher(row.teacher_no)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    // cancelled
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.teacher-index {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.toolbar {
  margin-bottom: 16px;
}
</style>