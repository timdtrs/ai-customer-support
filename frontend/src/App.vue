<template>
  <div class="app-layout flex flex-row h-screen overflow-hidden">
    <SidebarNavigation />
    <div class="main-content flex-1 h-screen overflow-y-auto">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import SidebarNavigation from './components/SidebarNavigation.vue'
</script>

<style>
body {
  font-family: "Inter", sans-serif !important;
}
</style>
