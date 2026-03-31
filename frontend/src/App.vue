<template>
  <div class="app-container">
    <el-container>
      <el-header height="60px" class="header">
        <div class="logo">AI知识学习与智能测评系统</div>
        <div class="user-info" v-if="user">
          <span>{{ user.username }}</span>
          <el-button type="text" @click="logout">退出登录</el-button>
        </div>
        <div class="login-register" v-else>
          <el-button type="primary" @click="navigateTo('/login')">登录</el-button>
          <el-button @click="navigateTo('/register')">注册</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="aside">
          <el-menu :default-active="activeMenu" class="menu" router>
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/study">
              <el-icon><Reading /></el-icon>
              <span>学习中心</span>
            </el-menu-item>
            <el-menu-item index="/practice">
              <el-icon><Edit /></el-icon>
              <span>章节刷题</span>
            </el-menu-item>
            <el-menu-item index="/special">
              <el-icon><CollectionTag /></el-icon>
              <span>专项训练</span>
            </el-menu-item>
            <el-menu-item index="/exam">
              <el-icon><Timer /></el-icon>
              <span>模拟考试</span>
            </el-menu-item>
            <el-menu-item index="/wrong">
              <el-icon><WarningFilled /></el-icon>
              <span>错题本</span>
            </el-menu-item>
            <el-menu-item index="/report">
              <el-icon><Document /></el-icon>
              <span>学习报告</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { HomeFilled, Reading, Edit, CollectionTag, Timer, WarningFilled, Document } from '@element-plus/icons-vue'
import { useUserStore } from './store/user'

const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user)
const activeMenu = computed(() => {
  const path = router.currentRoute.value.path
  return path || '/'
})

const navigateTo = (path) => {
  router.push(path)
}

const logout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  userStore.loadUser()
})
</script>

<style scoped>
.app-container {
  height: 100vh;
  overflow: hidden;
}

.header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.login-register {
  display: flex;
  gap: 10px;
}

.aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e4e7ed;
}

.menu {
  height: 100%;
  border-right: none;
}

.main {
  padding: 20px;
  overflow-y: auto;
}
</style>
