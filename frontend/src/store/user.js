import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    async login(email, password) {
      try {
        const response = await axios.post('/api/user/login', { email, password })
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        await this.loadUser()
        return { success: true }
      } catch (error) {
        console.error('登录失败:', error)
        let errorMessage = '登录失败，请检查邮箱和密码'
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        }
        return { success: false, error: errorMessage }
      }
    },
    async register(username, email, password) {
      try {
        const response = await axios.post('/api/user/register', { username, email, password })
        return { success: true }
      } catch (error) {
        console.error('注册失败:', error)
        let errorMessage = '注册失败，请稍后重试'
        
        if (error.response?.data?.detail) {
          // JSON格式的错误信息
          errorMessage = error.response.data.detail
        }
        
        return { success: false, error: errorMessage }
      }
    },
    async loadUser() {
      if (!this.token) return
      try {
        const response = await axios.get('/api/user/me', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        this.user = response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.logout()
      }
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
})
