import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

let authInterceptor = null

export async function setAuthInterceptor(token) {
  if (authInterceptor !== null) {
    instance.interceptors.request.eject(authInterceptor)
  }

  authInterceptor = instance.interceptors.request.use((config) => {
    config.headers.Authorization = `Token ${token}`
    // console.log('🔐 현재 토큰:', config.headers.Authorization)
    return config
  })
}

// 로그아웃 시 호출
export function clearAuthInterceptor() {
  if (authInterceptor !== null) {
    instance.interceptors.request.eject(authInterceptor)
    authInterceptor = null
  }
}

export default instance
