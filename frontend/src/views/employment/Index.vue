<template>
  <div class="employment-index">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>就业管理</el-breadcrumb-item>
    </el-breadcrumb>

    <search-form :fields="searchFields" @search="handleSearch" class="mb-4" />

    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">新增就业信息</el-button>
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
        <el-button link type="primary" @click="handleView(row)">查看</el-button>
        <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
      </template>
    </data-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SearchForm from '@/components/SearchForm.vue'
import DataTable from '@/components/DataTable.vue'
import { v2SearchEmployments } from '@/api/employment'
import type { EmploymentSearchResult } from '@/types/employment'

const router = useRouter()
const loading = ref(false)
const tableData = ref<EmploymentSearchResult[]>([])
const total = ref(0)
const searchData = ref<Record<string, unknown>>({})

const searchFields = [
  { prop: 'student_no', label: '学号', type: 'input', placeholder: '请输入学号' },
  { prop: 'company', label: '公司', type: 'input', placeholder: '请输入公司名称' },
  {
    prop: 'status',
    label: '状态',
    type: 'select',
    placeholder: '请选择状态',
    options: [
      { label: '待业', value: '待业' },
      { label: '在聘', value: '在聘' },
      { label: '已离职', value: '已离职' }
    ]
  }
]

const columns = [
  { prop: 'student_no', label: '学号', width: '120' },
  { prop: 'student_name', label: '姓名', width: '100' },
  { prop: 'class_no', label: '班级', width: '100' },
  { prop: 'company', label: '公司', minWidth: '150' },
  { prop: 'salary', label: '薪资', width: '100' },
  { prop: 'offer_time', label: '签约时间', width: '120' }
]

async function loadData() {
  loading.value = true
  try {
    const res = await v2SearchEmployments(searchData.value as any)
    tableData.value = res.data as EmploymentSearchResult[] || []
    total.value = tableData.value.length
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

function handlePageChange() {
  loadData()
}

function handleAdd() {
  router.push('/employment/form')
}

function handleView(row: EmploymentSearchResult) {
  router.push(`/employment/${row.student_no}`)
}

function handleEdit(row: EmploymentSearchResult) {
  router.push(`/employment/form/${row.student_no}`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
.employment-index {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.toolbar {
  margin-bottom: 16px;
}
</style>