<template>
  <div class="comment-item">
    <div class="comment-avatar"></div>
    <div class="comment-content">
      <div class="comment-user">{{ comment.user }}</div>
      <div class="comment-text">{{ comment.content }}</div>
      <div class="comment-date">{{ formatDate(comment.created_at) }}</div>
    </div>
    <button
      v-if="comment.user === userStore.userInfo?.username"
      class="comment-menu"
      @click="onDelete"
    >삭제
    </button>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useCommentStore } from '@/stores/comment'
import { useRoute } from 'vue-router'
const route = useRoute()
const props = defineProps({
  comment: Object,
})
const userStore = useUserStore()
const commentStore = useCommentStore()

const formatDate = (isoString) => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const onDelete = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    commentStore.deleteComment(route.params.threadId, props.comment.id)
  }
}
</script>

<style scoped>
.comment-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #ddd;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-user {
  font-weight: bold;
  font-size: 0.95rem;
  color: #3f2e1e; /* 따뜻한 짙은 갈색 */
}

.comment-text {
  margin-top: 4px;
  font-size: 0.95rem;
  color: #3f2e1e; /* 일관된 본문 텍스트 색상 */
}

.comment-date {
  font-size: 0.75rem;
  color: #a28c72; /* 흐릿한 모래색 */
  margin-top: 4px;
}

.comment-menu {
  font-size: 1rem;
  color: #a28c72; /* 모래빛 브라운 (placeholder와 통일) */
  cursor: pointer;
  padding: 0 0.4rem;
  user-select: none;
  transition: color 0.2s ease;
}

.comment-menu:hover {
  color: #6e4e2e; /* 진한 갈색으로 hover 효과 */
}

@media (max-width: 600px) {
  .comment-item {
    flex-direction: column;
    align-items: flex-start;
  }
  .comment-avatar {
    margin-bottom: 0.5rem;
  }
  .comment-menu {
    align-self: flex-end;
  }
}
</style>
