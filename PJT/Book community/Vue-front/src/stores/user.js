// src/stores/user.js
import { defineStore } from 'pinia'
import axios from '@/plugins/axios'
import { setAuthInterceptor, clearAuthInterceptor } from '@/plugins/axios'
import { computed, ref, watch } from 'vue'
import { useBookStore } from './book'
import { useThreadStore } from './thread'

export const useUserStore = defineStore('user', () => {
  const accessToken = ref('')  // ✅ 새로고침 대비
  const userInfo = ref({})  // ✅ 로그인한 사용자 전체 정보
  const isLogin = computed(() => {
    return accessToken.value ? true : false
  })

  const login = async (payload) => {
    const bookStore = useBookStore()
    const threadStore = useThreadStore()
    try {
      const res = await axios.post(`/accounts/login/`, payload)
      const token = res.data.key
      accessToken.value = token
      await setAuthInterceptor(token)
      await getUserInfo()
      await bookStore.getFavoriteBook()
      await threadStore.getThreadList()
    } catch (err) {
      // ✅ 콘솔 에러 대신 사용자에게 메시지로만 전달
      if (err.response && err.response.status === 400) {
        alert('아이디 또는 비밀번호가 잘못되었습니다.')
      } else {
        alert('로그인 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
      }

      // ❌ throw 제거하여 외부에서 다시 에러 catch하지 않게 함
    }
  }

  const signup = async ({ username, password1, password2, age, interested_categories }) => {
    const usernameRegex = /^[a-zA-Z0-9]{5,15}$/
    const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[\W_]).{8,}$/

    if (!usernameRegex.test(username)) {
      throw new Error('아이디는 5~15자의 영문 또는 숫자만 가능합니다.')
    }
    if (!passwordRegex.test(password1)) {
      throw new Error('비밀번호는 8자 이상, 영문/숫자/특수문자를 포함해야 합니다.')
    }
    if (password1 !== password2) {
      throw new Error('비밀번호가 일치하지 않습니다.')
    }

    const payload = {
      username,
      password1,
      password2,
      age: age || null,
      interested_categories: interested_categories || []
    }

    try {
      await axios.post(`/accounts/signup/`, payload)
    } catch (err) {
      if (err.response?.status === 400) {
        const detail = err.response.data
        const firstKey = Object.keys(detail)[0]
        const rawMessage = Array.isArray(detail[firstKey]) ? detail[firstKey][0] : '회원가입 오류가 발생했습니다.'

        let message = rawMessage
        if (rawMessage.includes('already exists')) {
          message = '이미 사용 중인 아이디입니다.'
        } else if (rawMessage.includes('This field may not be blank')) {
          message = '필수 입력 항목이 비어있습니다.'
        }

        throw new Error(message)
      } else {
        throw new Error('서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
      }
    }
  }


  // 🔍 현재 로그인한 사용자 정보 요청
  const getUserInfo = async () => {
    try {
      const res = await axios.get(`/accounts/user/`)
      userInfo.value = res.data
    } catch (err) {
      console.error('사용자 정보 요청 실패:', err)
      throw err
    }
  }

  // 🛠 사용자 정보 수정 요청
  const updateUserInfo = async (payload) => {
    try {
      const res = await axios.patch(`/accounts/user/`, payload)
      userInfo.value = res.data  // 최신 정보로 반영
    } catch (err) {
      console.error('사용자 정보 수정 실패:', err)
      throw err
    }
  }

  // 🚪 로그아웃
  const logout = async () => {
    const bookStore = useBookStore()
    const threadStore = useThreadStore()
    try {
      await axios.post('/accounts/logout/', null)
    } catch (err) {

    }
    accessToken.value = null
    clearAuthInterceptor()
    userInfo.value = null
    bookStore.clearFavoriteStatus()
    threadStore.clearLikeStatus()
    await bookStore.fetchBooks()
    await threadStore.getThreadList()
  }

  // 🔑 비밀번호 변경 요청 함수
  const changePassword = async ({ old_password, new_password1, new_password2 }) => {
    try {
      const res = await axios.post(`/accounts/password/change/`, {
        old_password,
        new_password1,
        new_password2
      })
      return res.data
    } catch (err) {
      console.error('비밀번호 변경 실패:', err)
      throw err
    }
  }

  const chatAi = async (method, message='') => {
    try {
      if (method === 'get') {
        const res = await axios.get('api/v1/chatbot/')
        return res.data
      } else if (method === 'post') {
        const res = await axios.post('/api/v1/chatbot/', { message })
        return res.data
      }
    } catch (err) {
      console.log(err)
    }
  }

  //  외부에서 사용할 상태와 함수들 반환
  return {
    accessToken, userInfo,
    isLogin, 
    login, signup, getUserInfo, updateUserInfo, logout,
    changePassword, chatAi
  }
}, {
  persist: true  // pinia-plugin-persistedstate 사용 시 필요
})
