<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top">
      <div class="container-fluid">
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
              <router-link to="/practice" class="nav-link" active-class="active">练习</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/exam" class="nav-link" active-class="active">考试</router-link>
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
    <main class="container-fluid pt-5 mt-5">
      <div class="row">
        <!-- 左侧边栏 -->
        <aside class="col-md-3 col-lg-2 bg-light border-right">
          <nav class="sidebar-sticky pt-5">
            <ul class="nav flex-column">
              <li class="nav-item mb-2">
                <router-link to="/study" class="nav-link d-flex align-items-center" active-class="active">
                  <span class="me-2">📚</span> 学习中心
                </router-link>
              </li>
              <li class="nav-item mb-2">
                <router-link to="/practice" class="nav-link d-flex align-items-center" active-class="active">
                  <span class="me-2">✏️</span> 专项练习
                </router-link>
              </li>
              <li class="nav-item mb-2">
                <router-link to="/exam" class="nav-link d-flex align-items-center" active-class="active">
                  <span class="me-2">📝</span> 模拟考试
                </router-link>
              </li>
              <li class="nav-item mb-2">
                <router-link to="/wrong" class="nav-link d-flex align-items-center" active-class="active">
                  <span class="me-2">❌</span> 错题集
                </router-link>
              </li>
              <li class="nav-item mb-2">
                <router-link to="/special" class="nav-link d-flex align-items-center" active-class="active">
                  <span class="me-2">⭐</span> 专题训练
                </router-link>
              </li>
              <li class="nav-item mb-2">
                <router-link to="/report" class="nav-link d-flex align-items-center" active-class="active">
                  <span class="me-2">📊</span> 学习报告
                </router-link>
              </li>
            </ul>
          </nav>
        </aside>

        <!-- 右侧内容区 -->
        <section class="col-md-9 col-lg-10">
          <div class="p-4">
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </div>
        </section>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="bg-light border-top mt-5">
      <div class="container-fluid py-4">
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
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

main {
  flex: 1;
}

.sidebar-sticky {
  position: sticky;
  top: 80px;
  height: calc(100vh - 80px);
  overflow-y: auto;
  padding-bottom: 2rem;
}

.nav-link {
  color: #495057;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  margin: 0.25rem 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-link:hover {
  color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  transform: translateX(5px);
}

.nav-link.active {
  color: #007bff;
  font-weight: 600;
  background-color: rgba(0, 123, 255, 0.15);
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
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

@media (max-width: 768px) {
  .sidebar-sticky {
    position: static;
    height: auto;
  }
  
  .nav-link {
    margin: 0.25rem 0;
  }
}
</style>

<style>
/* 全局样式 */
body {
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  line-height: 1.6;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

/* 自定义Bootstrap样式 */
.navbar {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  z-index: 1000;
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

.sidebar {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
}

/* 卡片样式 */
.card {
  border-radius: 0.75rem;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(5px);
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
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0069d9, #004a8f);
  border-color: #0062cc;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4);
}

.btn-outline-primary {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-outline-primary:hover {
  background: linear-gradient(135deg, #007bff, #0056b3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

/* 表单样式 */
.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.25rem rgba(0, 123, 255, 0.25);
  transition: all 0.3s ease;
}

/* 导航栏下拉菜单 */
.dropdown-menu {
  border-radius: 0.5rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  border: none;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.dropdown-item {
  transition: all 0.2s ease;
  border-radius: 0.25rem;
  margin: 0.25rem 0.5rem;
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
}

@media (max-width: 768px) {
  .navbar {
    background: rgba(255, 255, 255, 0.98) !important;
  }
  
  .sidebar {
    background: rgba(255, 255, 255, 0.98);
  }
}
</style>
