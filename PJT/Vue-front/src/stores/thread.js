import { defineStore } from "pinia"
import { ref } from "vue"
import { useRouter } from "vue-router"
import axios from '@/plugins/axios'

export const useThreadStore = defineStore('thread', () => {
  const BASE_URL = 'http://127.0.0.1:8000'
  const router = useRouter()
  const threadList = ref([])
  const thread = ref({})
  const likes = ref({})
  const threadHeatmap = ref({})


  const createThread = async (isCreate, id, { title, content, read_date }) => {
    try {
      // console.log(id)
      if (isCreate) {
        // 생성
        const res = await axios.post(`/api/v1/books/${id}/threads/`, { title, content, read_date }, 
          { headers: { 'Content-Type': 'application/json' } }
        )
        thread.value = res.data
      } else {
        // 수정
        const res = await axios.put(`/api/v1/threads/${id}/`, { title, content, read_date }, 
          { headers: { 'Content-Type': 'application/json' } }
        )
        thread.value = res.data
      }
      await getThreadList()
      router.push({ name: 'thread-detail', params: { threadId: thread.value.id } })
    } catch (err) {
      console.log(err)
    }
  }

  const getThreadList = async () => {
    try {
      const res = await axios.get(`/api/v1/threads/`)
      threadList.value = res.data
      res.data.forEach(item => {
      likes.value[item.id] = {
        liked: item.liked,           // 로그인한 사용자가 좋아요 눌렀는지
        like_count: item.like_count  // 총 좋아요 수
        }
      })
    } catch (err) {
      console.log(err)
    }
  }

  const getThreadDetail = async (threadId) => {
    try {
      const res = await axios.get(`api/v1/threads/${threadId}`)
      thread.value = res.data
      return res.data
    } catch (err) {
      console.log(err)
    }
  }

  const toggleLike = async (threadId) => {
    try {
      const res = await axios.post(`/api/v1/threads/${threadId}/like/`)
      likes.value[threadId] = {
        liked: res.data.liked,
        like_count: res.data.like_count
      }
    } catch (err) {
      console.error('좋아요 토글 실패:', err)
      throw err
    }
  }

  const deleteThread = async (threadId) => {
    try {
      await axios.delete(`/api/v1/threads/${threadId}/`)
      await getThreadList()
      return true
    } catch (err) {
      console.error('Thread 삭제 실패:', err)
      throw err
    }
  }

  const checkSpelling = async (content) => {
    try {
      const res = await axios.post(`/api/v1/threads/spell-check/`, { content })
      return res.data  // expected: { corrected, prefixes, suffixes }
    } catch (err) {
      console.error('맞춤법 검사 실패:', err)
      throw err
    }
  }

  const fetchThreadHeatmap = async () => {
    try {
      const res = await axios.get('/api/v1/threads/calendar/')
      // console.log(res.data)
      const heatmap = {}
      for (const entry of res.data) {
        heatmap[entry.read_date] = entry.count
      }
      threadHeatmap.value = heatmap
    } catch (err) {
      console.error('reading_calendar API 오류', err)
    }
  }

  const getThreadOnDate = async (date) => {
    try {
      const res = await axios.get(`/api/v1/threads/by-date/?date=${date}`)
      return res.data
    } catch (err) {
      console.error('데이터를 조회하는 데 실패했습니다: ', err)
    }
  }

  const getThreadSummary = async (threadId) => {
    try {
      await axios.post(`/api/v1/threads/${threadId}/analyze/`)
    } catch (err) {
      console.error(err)
    }
  }

  const getHotThreads = async () => {
    try {
      const res = await axios.get('/api/v1/threads/hot/')
      return res.data
    } catch (err) {
      console.error(err)
    }
  }

  const clearLikeStatus = () => {
    Object.keys(likes.value).forEach(threadId => {
      likes.value[threadId].liked = false
      // like_count는 서버 상태이므로 유지
    })
  }

  return {
    threadList, thread, BASE_URL, likes, threadHeatmap,
    createThread, getThreadList, getThreadDetail, toggleLike, 
    deleteThread, checkSpelling, fetchThreadHeatmap,
    getThreadOnDate, getThreadSummary, getHotThreads,
    clearLikeStatus, 
  }
}, { persist: true})