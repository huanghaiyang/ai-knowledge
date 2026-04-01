<template>
  <div class="register-container">
    <div class="register-bg"></div>
    <div class="register-card">
      <div class="register-header">
        <div class="logo">
          <span class="logo-icon">🎓</span>
          <h1>AI知识学习与智能测评系统</h1>
        </div>
        <h2 class="register-title">用户注册</h2>
        <p class="register-subtitle">创建账号，开启智能学习之旅</p>
      </div>
      <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-width="80px" class="register-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" class="custom-input" @input="formErrors.username = ''">
            <template #prefix>
              <span class="input-icon">👤</span>
            </template>
          </el-input>
          <div v-if="formErrors.username" class="error-message">{{ formErrors.username }}</div>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱" class="custom-input" @input="formErrors.email = ''">
            <template #prefix>
              <span class="input-icon">📧</span>
            </template>
          </el-input>
          <div v-if="formErrors.email" class="error-message">{{ formErrors.email }}</div>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" class="custom-input" @input="checkPasswordStrength; formErrors.password = ''">
            <template #prefix>
              <span class="input-icon">🔒</span>
            </template>
          </el-input>
          <div class="password-strength" v-if="registerForm.password">
            <div class="strength-bar">
              <div class="strength-indicator" :class="passwordStrengthClass"></div>
            </div>
            <div class="strength-text">{{ passwordStrengthText }}</div>
          </div>
          <div v-if="formErrors.password" class="error-message">{{ formErrors.password }}</div>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请确认密码" class="custom-input" @input="formErrors.confirmPassword = ''">
            <template #prefix>
              <span class="input-icon">🔐</span>
            </template>
          </el-input>
          <div v-if="formErrors.confirmPassword" class="error-message">{{ formErrors.confirmPassword }}</div>
        </el-form-item>
        <el-form-item class="register-button">
          <el-button type="primary" @click="register" :loading="loading" class="custom-button">
            <span v-if="!loading">注册</span>
            <span v-else>注册中...</span>
          </el-button>
        </el-form-item>
        <el-form-item class="login-link">
          <span>已有账号？</span>
          <el-button type="text" @click="navigateTo('/login')" class="login-button">立即登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const registerFormRef = ref(null)
const loading = ref(false)
const passwordStrength = ref('')
const formErrors = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度至少为3位', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少为8位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const checkPasswordStrength = (value) => {
  let strength = 0
  if (value.length >= 8) strength++
  if (/[A-Z]/.test(value)) strength++
  if (/[a-z]/.test(value)) strength++
  if (/\d/.test(value)) strength++
  if (/[!@#$%^&*()_+\-=\[\]{};:'",.<>?/\\|`~]/.test(value)) strength++
  
  switch (strength) {
    case 0:
    case 1:
      passwordStrength.value = 'weak'
      break
    case 2:
    case 3:
      passwordStrength.value = 'medium'
      break
    case 4:
    case 5:
      passwordStrength.value = 'strong'
      break
  }
}

const passwordStrengthClass = computed(() => {
  return `strength-${passwordStrength.value}`
})

const passwordStrengthText = computed(() => {
  switch (passwordStrength.value) {
    case 'weak':
      return '密码强度：弱'
    case 'medium':
      return '密码强度：中'
    case 'strong':
      return '密码强度：强'
    default:
      return ''
  }
})

const register = async () => {
  if (!registerFormRef.value) return
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      const registerResult = await userStore.register(
        registerForm.username,
        registerForm.email,
        registerForm.password
      )
      if (registerResult.success) {
        // 注册成功后直接登录
        const loginResult = await userStore.login(
          registerForm.email,
          registerForm.password
        )
        loading.value = false
        if (loginResult.success) {
          ElMessage.success('注册成功并已登录')
          router.push('/')
        } else {
          ElMessage.error('注册成功但登录失败，请手动登录')
          router.push('/login')
        }
      } else {
        loading.value = false
        // 显示后端返回的错误信息
        if (registerResult.error.includes('密码')) {
          formErrors.value.password = registerResult.error
        } else if (registerResult.error.includes('用户名')) {
          formErrors.value.username = registerResult.error
        } else if (registerResult.error.includes('邮箱')) {
          formErrors.value.email = registerResult.error
        } else {
          ElMessage.error(registerResult.error)
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
.register-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding-top: 10vh;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #e3e9f2 100%);
}

.register-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 20% 30%, rgba(0, 123, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 70%, rgba(108, 117, 125, 0.1) 0%, transparent 50%);
  z-index: 0;
}

.register-card {
  width: 420px;
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 32px;
  z-index: 1;
  animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.register-header {
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

.register-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.register-subtitle {
  font-size: 14px;
  color: #6c757d;
  margin: 0;
}

.register-form {
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

.password-strength {
  margin-top: 8px;
}

.strength-bar {
  height: 4px;
  background: #f8f9fa;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 4px;
}

.strength-indicator {
  height: 100%;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-weak {
  width: 33%;
  background: #dc3545;
}

.strength-medium {
  width: 66%;
  background: #ffc107;
}

.strength-strong {
  width: 100%;
  background: #28a745;
}

.strength-text {
  font-size: 12px;
  color: #6c757d;
}

.register-button {
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

.login-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #6c757d;
}

.login-button {
  color: #007bff;
  font-weight: 500;
  transition: all 0.3s ease;
}

.login-button:hover {
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
  .register-card {
    width: 90%;
    max-width: 400px;
    padding: 24px;
  }
  
  .logo h1 {
    font-size: 16px;
  }
  
  .register-title {
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
