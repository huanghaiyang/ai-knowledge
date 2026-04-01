<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top">
      <div class="container">
        <a class="navbar-brand" href="#">
          <h1 class="text-primary fw-bold mb-0">AI知识学习与智能测评系统</h1>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link" active-class="active">首页</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/study" class="nav-link" active-class="active">学习中心</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/practice" class="nav-link" active-class="active">专项练习</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/exam" class="nav-link" active-class="active">模拟考试</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/wrong" class="nav-link" active-class="active">错题集</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/special" class="nav-link" active-class="active">专题训练</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/report" class="nav-link" active-class="active">学习报告</router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                个人中心
              </a>
              <ul class="dropdown-menu">
                <template v-if="!isLoggedIn">
                  <li><router-link to="/login" class="dropdown-item">登录</router-link></li>
                  <li><router-link to="/register" class="dropdown-item">注册</router-link></li>
                </template>
                <template v-else>
                  <li><a class="dropdown-item" href="#">个人信息</a></li>
                  <li><a class="dropdown-item" href="#" @click="logout">退出登录</a></li>
                </template>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="container pt-5 mt-5">
      <div class="p-4">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="bg-light border-top mt-5">
      <div class="container py-4">
        <div class="row">
          <div class="col-md-6">
            <p class="text-muted mb-0">© 2026 AI知识学习与智能测评系统</p>
          </div>
          <div class="col-md-6 text-md-end">
            <p class="text-muted mb-0">设计参考：www.coze.cn</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from './store/user'
import { useRouter } from 'vue-router'

const store = useUserStore()
const router = useRouter()

const isLoggedIn = computed(() => store.isLoggedIn)

const logout = () => {
  store.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #e3e9f2 100%);
}

main {
  flex: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>

<style>
/* 全局样式 */
body {
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  line-height: 1.6;
  background: linear-gradient(135deg, #f5f7fa 0%, #e3e9f2 100%);
  min-height: 100vh;
}

/* 自定义Bootstrap样式 */
.navbar {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  z-index: 1000;
  padding: 0.75rem 0;
}

.navbar-brand h1 {
  font-size: 1.35rem;
  font-weight: 700;
  background: linear-gradient(135deg, #007bff, #0056b3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

/* 导航链接样式 */
.nav-link {
  color: #495057;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  margin: 0 0.25rem;
  font-weight: 500;
}

.nav-link:hover {
  color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  transform: translateY(-2px);
}

.nav-link.active {
  color: #007bff;
  font-weight: 600;
  background-color: rgba(0, 123, 255, 0.15);
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
}

/* 卡片样式 */
.card {
  border-radius: 0.75rem;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(5px);
  overflow: hidden;
}

.card:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-5px);
}

/* 按钮样式 */
.btn-primary {
  background: linear-gradient(135deg, #007bff, #0056b3);
  border-color: #007bff;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
  border-radius: 0.5rem;
  font-weight: 500;
  padding: 0.6rem 1.5rem;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0069d9, #004a8f);
  border-color: #0062cc;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4);
}

.btn-outline-primary {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 0.5rem;
  font-weight: 500;
  padding: 0.6rem 1.5rem;
}

.btn-outline-primary:hover {
  background: linear-gradient(135deg, #007bff, #0056b3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

/* 表单样式 */
.form-control {
  border-radius: 0.5rem;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  padding: 0.75rem 1rem;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.25rem rgba(0, 123, 255, 0.25);
  transform: translateY(-1px);
}

/* 导航栏下拉菜单 */
.dropdown-menu {
  border-radius: 0.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  border: none;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
  padding: 0.5rem 0;
  margin-top: 0.5rem;
}

.dropdown-item {
  transition: all 0.2s ease;
  border-radius: 0.25rem;
  margin: 0.25rem 0.5rem;
  padding: 0.5rem 1rem;
  font-weight: 500;
}

.dropdown-item:hover {
  background-color: rgba(0, 123, 255, 0.1);
  transform: translateX(5px);
}

/* 页脚样式 */
footer {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  margin-top: 2rem;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 加载动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 响应式调整 */
@media (max-width: 992px) {
  .navbar-brand h1 {
    font-size: 1.15rem;
  }
  
  .nav-link {
    padding: 0.5rem;
    margin: 0;
  }
}

@media (max-width: 768px) {
  .navbar {
    background: rgba(255, 255, 255, 0.98) !important;
    padding: 0.5rem 0;
  }
  
  .navbar-brand h1 {
    font-size: 1rem;
  }
  
  .nav-link {
    padding: 0.5rem 1rem;
  }
  
  main {
    padding-top: 1rem;
  }
}

/* 内容区域样式 */
.container {
  max-width: 1200px;
}

/* 卡片标题样式 */
.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1rem;
}

/* 卡片文本样式 */
.card-text {
  color: #6c757d;
  line-height: 1.6;
}

/* 阴影效果 */
.shadow-sm {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}

.shadow {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12) !important;
}

/* 过渡效果 */
.transition-all {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 圆角样式 */
.rounded-lg {
  border-radius: 0.75rem !important;
}

/* 间距样式 */
.mt-5 {
  margin-top: 3rem !important;
}

.mb-5 {
  margin-bottom: 3rem !important;
}

/* 背景色样式 */
.bg-white {
  background-color: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(5px);
}

/* 文字颜色样式 */
.text-primary {
  color: #007bff !important;
}

.text-secondary {
  color: #6c757d !important;
}

/* 字体粗细 */
.font-weight-medium {
  font-weight: 500 !important;
}

.font-weight-semibold {
  font-weight: 600 !important;
}
</style>
