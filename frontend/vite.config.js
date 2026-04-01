import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

// 读取配置文件
let config = {}
try {
  const configPath = path.resolve(process.cwd(), 'config.json')
  if (fs.existsSync(configPath)) {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'))
  }
} catch (error) {
  console.error('配置文件解析失败，使用环境变量或默认值')
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd())
  
  return {
    plugins: [vue()],
    server: {
      port: parseInt(env.VITE_FRONTEND_PORT || config.frontend?.port || '3000'),
      proxy: {
        '/api': {
          target: env.VITE_BACKEND_URL || (config.backend?.host && config.backend?.port ? `${config.backend?.protocol || 'http'}://${config.backend.host}:${config.backend.port}` : 'http://localhost:8000'),
          changeOrigin: true
        }
      }
    }
  }
})
