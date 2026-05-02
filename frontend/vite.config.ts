import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from "node:path"

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  // 配置路径别名，使用 '@' 代表 'src' 目录
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    // 配置开发服务器的代理，将 API 请求转发到后端服务器
    proxy: {
      // 将以 /api 开头的请求代理到 http://localhost:3000
      '/api': "http://localhost:8088/api",
      "/oss": "http://localhost:8088/oss"
    }
  }
})
