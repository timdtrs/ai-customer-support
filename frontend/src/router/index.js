import { createRouter, createWebHistory } from 'vue-router'

// Importieren Sie hier Ihre Komponenten
import Dashboard from '../views/Dashboard.vue'

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
    }
  ]
})

export default router
