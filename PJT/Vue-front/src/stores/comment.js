import { defineStore } from 'pinia'
import { reactive } from 'vue'
import axios from '@/plugins/axios'

export const useCommentStore = defineStore('comment', () => {
  // ✅ threadId 기준으로 댓글 저장
  const commentMap = reactive({})

  // ✅ 댓글 가져오기 (캐시 + 오류 대응 포함)
  const fetchComments = async (threadId, force = false) => {
    if (!force && commentMap[threadId]) return  // 이미 있음 → skip

    try {
      const res = await axios.get(`/api/v1/threads/${threadId}/comments/`)
      commentMap[threadId] = res.data
    } catch (err) {
      if (err.response?.status === 404) {
        commentMap[threadId] = []  // 존재하지만 비어있음
      } else {
        console.warn('댓글 요청 실패:', err)
      }
    }
  }

  const createComment = async (threadId, content) => {
    const res = await axios.post(`/api/v1/threads/${threadId}/comments/`, { content })
    commentMap[threadId] = [...(commentMap[threadId] || []), res.data]
  }

  const deleteComment = async (threadId, commentId) => {
    console.log(commentId)
    await axios.delete(`/api/v1/comments/${commentId}/`)
    if (commentMap[threadId]) {
      commentMap[threadId] = commentMap[threadId].filter(c => c.id !== commentId)
    }
  }

  return {
    commentMap,
    fetchComments,
    createComment,
    deleteComment
  }
})