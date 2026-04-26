<template>
  <div class="statistics-index">
    <el-breadcrumb separator="/" class="mb-4">
      <el-breadcrumb-item>首页</el-breadcrumb-item>
      <el-breadcrumb-item>统计分析</el-breadcrumb-item>
    </el-breadcrumb>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>班级性别统计</span>
          </template>
          <div ref="genderChart" class="chart-container" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>班级平均分</span>
          </template>
          <div ref="scoreChart" class="chart-container" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>薪资排行 TOP10</span>
          </template>
          <div ref="salaryChart" class="chart-container" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>班级就业时长</span>
          </template>
          <div ref="durationChart" class="chart-container" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { getClassGender, getClassAvgScore, getTopSalary, getClassOfferDuration } from '@/api/statistics'

const genderChart = ref<HTMLElement>()
const scoreChart = ref<HTMLElement>()
const salaryChart = ref<HTMLElement>()
const durationChart = ref<HTMLElement>()

async function loadCharts() {
  try {
    const [genderRes, scoreRes, salaryRes, durationRes] = await Promise.all([
      getClassGender(),
      getClassAvgScore(),
      getTopSalary(10),
      getClassOfferDuration()
    ])

    const genderData = genderRes.data || []
    const scoreData = scoreRes.data || []
    const salaryData = salaryRes.data || []
    const durationData = durationRes.data || []

    if (genderChart.value) {
      const chart = echarts.init(genderChart.value)
      chart.setOption({
        tooltip: {},
        xAxis: { type: 'category', data: genderData.map((d: any) => d.class_name) },
        yAxis: { type: 'value' },
        series: [
          { name: '男', type: 'bar', data: genderData.map((d: any) => d.male_count) },
          { name: '女', type: 'bar', data: genderData.map((d: any) => d.female_count) }
        ]
      })
    }

    if (scoreChart.value) {
      const chart = echarts.init(scoreChart.value)
      chart.setOption({
        tooltip: {},
        xAxis: { type: 'category', data: scoreData.map((d: any) => d.class_name) },
        yAxis: { type: 'value' },
        series: [{ type: 'bar', data: scoreData.map((d: any) => d.avg_score) }]
      })
    }

    if (salaryChart.value) {
      const chart = echarts.init(salaryChart.value)
      chart.setOption({
        tooltip: {},
        yAxis: { type: 'category', data: salaryData.map((d: any) => d.name) },
        xAxis: { type: 'value' },
        series: [{ type: 'bar', data: salaryData.map((d: any) => d.salary) }]
      })
    }

    if (durationChart.value) {
      const chart = echarts.init(durationChart.value)
      chart.setOption({
        tooltip: {},
        xAxis: { type: 'category', data: durationData.map((d: any) => d.class_name) },
        yAxis: { type: 'value' },
        series: [{ type: 'bar', data: durationData.map((d: any) => d.avg_duration_days) }]
      })
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadCharts()
})
</script>

<style scoped lang="scss">
.statistics-index {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.mt-4 {
  margin-top: 16px;
}

.chart-container {
  height: 300px;
}
</style>