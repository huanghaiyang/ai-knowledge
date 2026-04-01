<template>
  <div class="login-container">
    <div class="login-bg"></div>
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <span class="logo-icon">🎓</span>
          <h1>AI知识学习与智能测评系统</h1>
        </div>
        <h2 class="login-title">用户登录</h2>
        <p class="login-subtitle">登录账号，继续智能学习之旅</p>
      </div>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px" class="login-form">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="loginForm.email" placeholder="请输入邮箱" class="custom-input" @input="formErrors.email = ''">
            <template #prefix>
              <span class="input-icon">📧</span>
            </template>
          </el-input>
          <div v-if="formErrors.email" class="error-message">{{ formErrors.email }}</div>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" class="custom-input" @input="formErrors.password = ''">
            <template #prefix>
              <span class="input-icon">🔒</span>
            </template>
          </el-input>
          <div v-if="formErrors.password" class="error-message">{{ formErrors.password }}</div>
        </el-form-item>
        <el-form-item class="login-button">
          <el-button type="primary" @click="login" :loading="loading" class="custom-button">
            <span v-if="!loading">登录</span>
            <span v-else>登录中...</span>
          </el-button>
        </el-form-item>
        <el-form-item class="register-link">
          <span>还没有账号？</span>
          <el-button type="text" @click="navigateTo('/register')" class="register-button">立即注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref(null)
const loading = ref(false)
const formErrors = ref({
  email: '',
  password: ''
})

const loginForm = reactive({
  email: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少为8位', trigger: 'blur' }
  ]
}

const login = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      const result = await userStore.login(loginForm.email, loginForm.password)
      loading.value = false
      if (result.success) {
        router.push('/')
      } else {
        // 显示后端返回的错误信息
        if (result.error.includes('邮箱') || result.error.includes('密码')) {
          ElMessage.error(result.error)
        } else {
          ElMessage.error('登录失败，请检查邮箱和密码')
        }
      }
    }
  })
}

const navigateTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding-top: 10vh;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #e3e9f2 100%);
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 20% 30%, rgba(0, 123, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 70%, rgba(108, 117, 125, 0.1) 0%, transparent 50%);
  z-index: 0;
}

.login-card {
  width: 420px;
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 32px;
  z-index: 1;
  animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.logo-icon {
  font-size: 32px;
  margin-right: 12px;
}

.logo h1 {
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, #007bff, #0056b3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.login-subtitle {
  font-size: 14px;
  color: #6c757d;
  margin: 0;
}

.login-form {
  margin-top: 16px;
}

.custom-input {
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 48px;
}

.custom-input:hover {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
}

.custom-input:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
}

.input-icon {
  font-size: 16px;
  color: #6c757d;
}

.login-button {
  margin-top: 24px;
  margin-bottom: 16px;
}

.custom-button {
  width: 100%;
  height: 48px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #007bff, #0056b3);
  border: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.custom-button:hover {
  background: linear-gradient(135deg, #0069d9, #004a8f);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4);
}

.custom-button:active {
  transform: translateY(0);
}

.register-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #6c757d;
}

.register-button {
  color: #007bff;
  font-weight: 500;
  transition: all 0.3s ease;
}

.register-button:hover {
  color: #0056b3;
  text-decoration: underline;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-form-item__label {
  font-weight: 500;
  color: #495057;
}

.el-message {
  min-width: 300px;
}

.error-message {
  color: #f56c6c;
  font-size: 12px;
  line-height: 1;
  padding-top: 4px;
  margin-top: 4px;
  font-weight: 400;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .login-card {
    width: 90%;
    max-width: 400px;
    padding: 24px;
  }
  
  .logo h1 {
    font-size: 16px;
  }
  
  .login-title {
    font-size: 20px;
  }
  
  .custom-button {
    height: 44px;
    font-size: 14px;
  }
  
  .custom-input {
    height: 44px;
  }
}
</style>
