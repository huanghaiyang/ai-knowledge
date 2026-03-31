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
        return true
      } catch (error) {
        console.error('登录失败:', error)
        return false
      }
    },
    async register(username, email, password) {
      try {
        const response = await axios.post('/api/user/register', { username, email, password })
        return true
      } catch (error) {
        console.error('注册失败:', error)
        return false
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
