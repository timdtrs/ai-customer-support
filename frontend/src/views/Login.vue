<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <div class=" p-8 rounded w-full max-w-sm">
      <h1 class="text-2xl font-bold mb-6 text-center">Solvee Login</h1>
      <Button class="w-full" @click="login">Log in mit Auth0</Button>
    </div>
  </div>
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue';

export default {
  setup() {
    const { loginWithRedirect } = useAuth0();
    return {
      login: () => loginWithRedirect(),
    };
  },
};
</script>

<style scoped>
body {
  background: #f9fafb;
}
</style>
