import { createRouter, createWebHistory } from 'vue-router'

// Importieren Sie hier Ihre Komponenten
import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { watch } from 'vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/playground',
      name: 'playground',
      component: () => import('../views/Playground.vue'),
      children: [
        {
          path: 'config',
          name: 'playground-config',
          component: () => import('../views/PlaygroundConfig.vue')
        },
        {
          path: 'export',
          name: 'playground-export',
          component: () => import('../views/PlaygroundExport.vue')
        },
        {
          path: '',
          redirect: { name: 'playground-config' }
        }
      ]
    },
    {
      path: '/vorgaenge',
      name: 'vorgaenge',
      component: () => import('../views/Vorgaenge.vue')
    },
    {
      path: '/vorgaenge/:id',
      name: 'vorgang-details',
      component: () => import('../views/VorgangDetails.vue'),
      props: true
    },
    {
      path: '/wissensbasis',
      name: 'wissensbasis',
      component: () => import('../views/Wissensbasis.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }
  ]
})

// Navigation Guard für Authentifizierung
router.beforeEach((to, from, next) => {
  const { isAuthenticated, isLoading } = useAuth0();

  function checkAuth() {
    if (to.name !== 'login' && !isAuthenticated.value) {
      next({ name: 'login' });
    } else if (to.name === 'login' && isAuthenticated.value) {
      next({ name: 'dashboard' });
    } else {
      next();
    }
  }

  if (isLoading.value) {
    const stop = watch(isLoading, (val) => {
      if (!val) {
        stop();
        checkAuth();
      }
    });
    return;
  }
  checkAuth();
});

export default router
