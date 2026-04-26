<template>
  <div class="data-table">
    <el-table
      v-loading="loading"
      :data="data"
      :border="border"
      stripe
      @selection-change="handleSelectionChange"
    >
      <el-table-column v-if="showSelection" type="selection" width="55" />
      <el-table-column
        v-for="col in columns"
        :key="col.prop"
        :prop="col.prop"
        :label="col.label"
        :width="col.width"
        :min-width="col.minWidth"
        :align="col.align || 'left'"
      >
        <template v-if="col.slot" #default="scope">
          <slot :name="col.prop" :row="scope.row" />
        </template>
      </el-table-column>
      <el-table-column v-if="showAction" label="操作" :width="actionWidth" fixed="right">
        <template #default="scope">
          <slot name="action" :row="scope.row" />
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-if="showPagination"
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      class="pagination"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Column {
  prop: string
  label: string
  width?: string | number
  minWidth?: string | number
  align?: 'left' | 'center' | 'right'
  slot?: boolean
}

interface Props {
  data: Record<string, unknown>[]
  columns: Column[]
  loading?: boolean
  total?: number
  showSelection?: boolean
  showAction?: boolean
  showPagination?: boolean
  actionWidth?: string | number
  border?: boolean
}

interface Emits {
  (e: 'selection-change', rows: Record<string, unknown>[]): void
  (e: 'page-change', page: number, pageSize: number): void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  total: 0,
  showSelection: false,
  showAction: false,
  showPagination: false,
  actionWidth: 200,
  border: true
})

const emit = defineEmits<Emits>()

const currentPage = ref(1)
const pageSize = ref(20)

watch(() => props.total, () => {
  currentPage.value = 1
})

function handleSelectionChange(rows: Record<string, unknown>[]) {
  emit('selection-change', rows)
}

function handlePageChange(page: number) {
  emit('page-change', page, pageSize.value)
}

function handleSizeChange(size: number) {
  currentPage.value = 1
  emit('page-change', currentPage.value, size)
}
</script>

<style scoped lang="scss">
.data-table {
  width: 100%;
}

.pagination {
  margin-top: 16px;
  justify-content: flex-end;
}
</style>