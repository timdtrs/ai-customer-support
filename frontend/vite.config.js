import { fileURLToPath, URL } from 'node:url'
import tailwindcss from "@tailwindcss/vite";
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const target = env.VITE_API_URL || 'http://backend:8000'
  return {
    plugins: [
      vue(),
      vueDevTools(),
      tailwindcss(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      proxy: {
        '/api': {
          target,
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, ''),
        },
      },
      watch: {
        usePolling: true,
      },
    },
  }
})
