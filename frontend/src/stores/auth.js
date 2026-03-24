import { defineStore } from 'pinia'
import { loginApi, meApi, registerApi } from '../api/authService'

const toError = (error) => error?.message || '操作失败，请稍后重试'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || '',
    user: JSON.parse(localStorage.getItem('auth_user') || 'null'),
    loading: false,
    error: ''
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token)
  },
  actions: {
    setAuth(token, user) {
      this.token = token
      this.user = user
      localStorage.setItem('auth_token', token)
      localStorage.setItem('auth_user', JSON.stringify(user))
    },
    clearAuth() {
      this.token = ''
      this.user = null
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
    },
    async login(payload) {
      this.loading = true
      this.error = ''
      try {
        const data = await loginApi(payload)
        this.setAuth(data.token, data.user)
      } catch (error) {
        this.error = toError(error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async register(payload) {
      this.loading = true
      this.error = ''
      try {
        const data = await registerApi(payload)
        this.setAuth(data.token, data.user)
      } catch (error) {
        this.error = toError(error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async fetchMe() {
      if (!this.token) return
      try {
        const user = await meApi()
        this.user = user
        localStorage.setItem('auth_user', JSON.stringify(user))
      } catch {
        this.clearAuth()
      }
    }
  }
})
