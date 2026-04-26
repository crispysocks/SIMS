<template>
  <router-view v-if="$route.path === '/login'" />
  <app-layout v-else />
</template>

<script setup lang="ts">
import AppLayout from '@/components/AppLayout.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial,
    sans-serif;
}
</style>