<template>
  <div class="classes-index">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>班级管理</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增班级</el-button>
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
import { getClasses, deleteClass } from '@/api/classes'
import type { ClassInfo } from '@/types/classes'

const router = useRouter()
const loading = ref(false)
const tableData = ref<ClassInfo[]>([])
const total = ref(0)

const columns = [
  { prop: 'class_no', label: '班级编号', width: '120' },
  { prop: 'class_name', label: '班级名称', minWidth: '150' },
  { prop: 'class_open_time', label: '开课时间', width: '120' },
  { prop: 'head_teacher_no', label: '班主任', width: '100' },
  { prop: 'instructor_no', label: '授课老师', width: '100' },
  { prop: 'description', label: '描述', minWidth: '200' }
]

async function loadData() {
  loading.value = true
  try {
    const res = await getClasses()
    tableData.value = res.data as ClassInfo[] || []
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
  router.push('/classes/form')
}

function handleEdit(row: ClassInfo) {
  router.push(`/classes/form/${row.class_no}`)
}

async function handleDelete(row: ClassInfo) {
  try {
    await ElMessageBox.confirm('确定要删除该班级吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteClass(row.class_no)
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
.classes-index {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.toolbar {
  margin-bottom: 16px;
}
</style>