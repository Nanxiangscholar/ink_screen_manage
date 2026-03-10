import axios from 'axios'

// 创建 axios 实例
const service = axios.create({
  baseURL: '',
  timeout: 10000,
  withCredentials: true // 允许携带凭证
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 可以在这里添加 token 等认证信息
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.success !== true) {
      // 处理错误响应
      console.error('响应错误:', res.message)
    }
    return res
  },
  error => {
    console.error('响应错误:', error)
    return Promise.reject(error)
  }
)

export default service