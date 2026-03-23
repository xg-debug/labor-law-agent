import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: Number(import.meta.env.VITE_API_TIMEOUT || 20000)
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      return Promise.reject(new Error('请求超时，请稍后重试'))
    }
    if (error.response?.data?.detail) {
      return Promise.reject(new Error(error.response.data.detail))
    }
    return Promise.reject(new Error(error.message || '请求失败'))
  }
)

export default client
