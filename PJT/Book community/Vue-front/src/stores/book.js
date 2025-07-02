import { defineStore } from 'pinia'
import axios from '@/plugins/axios'
import { ref } from 'vue'
import { walk } from 'vue/compiler-sfc'

export const useBookStore = defineStore('book', () => {
  const books = ref([])
  const categories = ref([])
  const book = ref({})
  const favorites = ref({})
  const totalPages = ref(0)
  //  추가: 유사 도서 리스트 상태
  const recommendedBooks = ref([])
  const userFavoriteBookList = ref([])

  const fetchBannerBooks = async () => {
    try {
      const res = await axios.get('api/v1/books/')
      return res.data.results.slice(0, 10)
    } catch (err) {
      return
    }
  }

  // 도서 목록 조회 함수
  const fetchBooks = async (page = 1, query = '', category = '') => {
    try {
      const res = await axios.get(`/api/v1/books/?page=${page}&query=${query}&category=${category}`)
      books.value = res.data.results
      totalPages.value = res.data.num_pages
      res.data.results.forEach(item => {
        favorites.value[item.id] = {
          favorited: item.favorited,
          favorite_count: item.favorite_count
        }
      })
    } catch (err) {
      // console.error('도서 목록 조회 실패:', err)
    }
  }

  const getBookDetailData = async (bookId) => {
    try {
      const res = await axios.get(`/api/v1/books/${bookId}/`)
      book.value = res.data
    } catch (err) {
      // console.log(err)
    }
  }

  const getCategoryData = async () => {
    if (categories.value.length > 0) return 
    try {
      const res = await axios.get(`/api/v1/categories/`)
      categories.value = res.data
    } catch (err) {
      console.error(err)
    }
  }

  const getFavoriteBook = async () => {
    try {
      const res = await axios.get('/api/v1/books/favorites/')
      userFavoriteBookList.value = res.data
      // return res.data  // ✅ 정상 응답이면 배열 리턴
    } catch (err) {
      if (err.response?.status === 404) {
        return []  // 찜한 책이 없는 경우
      } else {
        // console.error('찜한 도서 조회 실패:', err)
        return []
      }
    }
  }

  const toggleFavorite = async (bookId) => {
    try {
      const res = await axios.post(`/api/v1/books/${bookId}/favorite/`)
      const { favorited, favorite_count } = res.data

      getFavoriteBook()
      // 1. 상태 즉시 반영
      favorites.value[bookId] = { favorited, favorite_count }
      // 2. 찜한 도서 목록 상태 반영
      const updatedBook = books.value.find(book => book.id === bookId)
      if (updatedBook) {
        // books에서 찾은 경우 복사해서 반영
        const copy = { ...updatedBook, favorited, favorite_count }
        if (favorited) {
          // 찜 추가
          if (!userFavoriteBookList.value.find(book => book.id === bookId)) {
            userFavoriteBookList.value.push(copy)
          }
        } else {
          // 찜 해제
          userFavoriteBookList.value = userFavoriteBookList.value.filter(book => book.id !== bookId)
        }
      }

      return { favorited, favorite_count }
    } catch (err) {
      // console.error('책 찜 토글 실패:', err)
      throw err
    }
  }

  //  추가: 유사 도서 API 호출 함수
  const getRecommendedBooks = async (bookId) => {
    try {
      const res = await axios.get(`/api/v1/books/${bookId}/recommend-pickle/`)
      recommendedBooks.value = res.data
    } catch (err) {
      console.error('유사 도서 추천 조회 실패:', err)
      recommendedBooks.value = []  // 실패 시 빈 배열 처리
    }
  }
  const fetchUserRecommendedBooks = async () => {
    try {
      const res = await axios.get('/api/v1/books/recommend-interest/')
      return res
    } catch (err) {
      console.error('추천 도서 불러오기 실패:', err)
      return []
    }
  }

  const fetchYouTubeVideo = async (query) => {
    try {
      const res = await axios.get('/api/v1/youtube/', {
        params: { query }
      })
      return res
    } catch (err) {
      // console.error(err)
      return null
    }
  }
    // 찜 상태 초기화 함수
  const clearFavoriteStatus = () => {
    // 목록 전체 초기화
    books.value.forEach(book => {
      favorites.value[book.id] = {
        favorited: false,
      }
    })

    // 단일 책 상세도 초기화
    book.value.favorited = false

    // 찜한 책 목록 비우기
    userFavoriteBookList.value = []
  }
  return {
    books, book, categories, favorites, totalPages,
    userFavoriteBookList, recommendedBooks,
    fetchBooks, getBookDetailData, getCategoryData, 
    getFavoriteBook, toggleFavorite, fetchBannerBooks, 
    getRecommendedBooks, fetchUserRecommendedBooks, 
    fetchYouTubeVideo, clearFavoriteStatus,
  }
}, { persist: true })



