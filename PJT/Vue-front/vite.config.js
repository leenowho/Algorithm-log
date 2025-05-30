import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import path from 'path'  // ⬅️ 이거 꼭 필요

export default defineConfig({
  plugins: [ vue(), vueDevTools() ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // ⬅️ @를 src 폴더로 매핑
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
