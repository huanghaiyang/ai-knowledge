import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/study',
    name: 'Study',
    component: () => import('../views/Study.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('../views/Practice.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/special',
    name: 'Special',
    component: () => import('../views/Special.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/exam',
    name: 'Exam',
    component: () => import('../views/Exam.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wrong',
    name: 'Wrong',
    component: () => import('../views/Wrong.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/report',
    name: 'Report',
    component: () => import('../views/Report.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  if (requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
