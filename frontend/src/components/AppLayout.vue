<template>
  <el-container class="app-layout">
    <app-header />
    <el-container>
      <app-sidebar />
      <el-main class="main-container">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
</script>

<style scoped lang="scss">
.app-layout {
  height: 100vh;
}

.main-container {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>