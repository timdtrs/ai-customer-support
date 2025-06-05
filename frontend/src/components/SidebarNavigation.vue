<template>
  <aside class="sidebar flex flex-col p-3 bg-white h-screen">
    <div class="sidebar-header flex justify-center items-center mb-3">
      <h2 class="font-bold text-4xl">Solvee</h2>
    </div>
    <nav class="mt-6">
      <ul class="flex flex-col gap-2">
        <li>
          <router-link class="nav-link flex items-center gap-3 px-3 py-2 rounded-lg transition-colors" :to="{ name: 'dashboard' }" active-class="active">
            <i class="pi pi-chart-bar text-lg"></i>
            Dashboard
          </router-link>
        </li>
        <li hidden>
          <router-link class="nav-link flex items-center gap-3 px-3 py-2 rounded-lg transition-colors" :to="{ name: 'vorgaenge' }" active-class="active">
            <i class="pi pi-list text-lg"></i>
            Vorgänge
          </router-link>
        </li>
        <li>
          <router-link
            class="nav-link flex items-center gap-3 px-3 py-2 rounded-lg transition-colors"
            :to="{ name: 'playground-config' }"
            :class="{ active: $route.path.startsWith('/playground') }"
          >
            <i class="pi pi-cog text-lg"></i>
            Playground
          </router-link>
        </li>
        <li>
          <router-link class="nav-link flex items-center gap-3 px-3 py-2 rounded-lg transition-colors" :to="{ name: 'wissensbasis' }" active-class="active">
            <i class="pi pi-book text-lg"></i>
            Wissensbasis
          </router-link>
        </li>
      </ul>
    </nav>
    <div>
      
    
  </div>
  <div class="mt-auto w-full">
        <Button class="w-full" v-if="!isAuthenticated" @click="login">Log in</Button>
        <Button class="w-full" severity="secondary" v-else @click="logout">Log out</Button>
      </div>
  </aside>
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue';
import { computed } from 'vue';

export default {
  setup() {
    const { loginWithRedirect, isAuthenticated, logout } = useAuth0();

    return {
      login: () => {
        loginWithRedirect();
      },
      logout: () => {
        logout({ returnTo: window.location.origin });
      },
      isAuthenticated: computed(() => isAuthenticated.value),
    };
  }
};
</script>

<style scoped>
.sidebar {
  min-height: 100vh;
  width: 240px;
}
.nav-link {
  color: #333;
  font-weight: 500;
  text-decoration: none;
}
.nav-link:hover,
.active {
  background-color: var(--p-neutral-100);
  color: #000000 !important;
  font-weight: 500;
}
.active i {
  font-weight: bold;
}
</style>
