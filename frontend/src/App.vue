<template>
  <div class="app-layout flex flex-row h-screen overflow-hidden">
    <SidebarNavigation v-if="isAuthenticated" />
    <div class="main-content flex-1 h-screen overflow-y-auto">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import SidebarNavigation from './components/SidebarNavigation.vue'
import { useAuth0 } from '@auth0/auth0-vue'
import { computed } from 'vue'

const { isAuthenticated } = useAuth0()
// Optional: computed, falls du reaktive Nutzung willst
// const isAuth = computed(() => isAuthenticated.value)
</script>

<style>
body {
  font-family: "Inter", sans-serif !important;
}
</style>
