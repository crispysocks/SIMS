<template>
  <div class="search-form">
    <el-form :inline="true" :model="formData" @submit.prevent="handleSearch">
      <el-form-item
        v-for="field in fields"
        :key="field.prop"
        :label="field.label"
      >
        <el-input
          v-if="field.type === 'input'"
          v-model="formData[field.prop]"
          :placeholder="field.placeholder"
          clearable
        />
        <el-select
          v-else-if="field.type === 'select'"
          v-model="formData[field.prop]"
          :placeholder="field.placeholder"
          clearable
        >
          <el-option
            v-for="opt in field.options"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
          />
        </el-select>
        <el-date-picker
          v-else-if="field.type === 'date'"
          v-model="formData[field.prop]"
          type="date"
          :placeholder="field.placeholder"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Field {
  prop: string
  label: string
  type: 'input' | 'select' | 'date'
  placeholder?: string
  options?: { label: string; value: string | number }[]
}

interface Props {
  fields: Field[]
  modelValue?: Record<string, unknown>
}

interface Emits {
  (e: 'search', data: Record<string, unknown>): void
  (e: 'update:modelValue', data: Record<string, unknown>): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const formData = ref<Record<string, unknown>>({})

watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal }
  }
}, { immediate: true, deep: true })

function handleSearch() {
  emit('search', formData.value)
  emit('update:modelValue', formData.value)
}

function handleReset() {
  formData.value = {}
  emit('search', formData.value)
  emit('update:modelValue', formData.value)
}
</script>

<style scoped lang="scss">
.search-form {
  margin-bottom: 20px;
}
</style>