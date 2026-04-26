<template>
  <el-aside :width="appStore.sidebarCollapsed ? '64px' : '200px'" class="app-sidebar">
    <el-menu
      :default-active="activeMenu"
      :collapse="appStore.sidebarCollapsed"
      router
      class="sidebar-menu"
    >
      <el-menu-item index="/">
        <el-icon><House /></el-icon>
        <template #title>首页</template>
      </el-menu-item>
      <el-menu-item index="/students">
        <el-icon><User /></el-icon>
        <template #title>学生管理</template>
      </el-menu-item>
      <el-menu-item index="/teachers">
        <el-icon><Avatar /></el-icon>
        <template #title>教师管理</template>
      </el-menu-item>
      <el-menu-item index="/classes">
        <el-icon><Collection /></el-icon>
        <template #title>班级管理</template>
      </el-menu-item>
      <el-menu-item index="/scores">
        <el-icon><Memo /></el-icon>
        <template #title>成绩管理</template>
      </el-menu-item>
      <el-menu-item index="/employment">
        <el-icon><Briefcase /></el-icon>
        <template #title>就业管理</template>
      </el-menu-item>
      <el-menu-item index="/statistics">
        <el-icon><DataAnalysis /></el-icon>
        <template #title>统计分析</template>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import {
  House,
  User,
  Avatar,
  Collection,
  Memo,
  Briefcase,
  DataAnalysis
} from '@element-plus/icons-vue'

const route = useRoute()
const appStore = useAppStore()

const activeMenu = computed(() => route.path)
</script>

<style scoped lang="scss">
.app-sidebar {
  background-color: #fff;
  transition: width 0.3s;
  overflow: hidden;
}

.sidebar-menu {
  border-right: none;
  height: 100%;
}
</style>