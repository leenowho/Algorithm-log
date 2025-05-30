<template>
  <div class="comment-list">
    <div class="comment-form">
      <template v-if="userStore.isLogin">
        <form @submit.prevent="submitComment" class="comment-form-inner">
          <input
            v-model="newComment"
            placeholder="댓글을 작성해주세요"
            class="comment-input"
          />
          <button class="comment-button">등록</button>
        </form>
      </template>
      <template v-else>
        <p class="login-warning">※ 로그인 후 댓글을 작성할 수 있습니다.</p>
      </template>
    </div>
    <div v-if="commentStore.commentMap[threadId]?.length">
      <CommentItem
        v-for="comment in commentStore.commentMap[threadId]"
        :key="comment.id"
        :comment="comment"
      />
    </div>
    <p v-else class="no-comment-text">아직 작성된 댓글이 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCommentStore } from '@/stores/comment'
import { useUserStore } from '@/stores/user'
import CommentItem from '@/components/comments/CommentItem.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const commentStore = useCommentStore()
const userStore = useUserStore()
const threadId = ref(route.params.threadId)

const newComment = ref('')

const submitComment = async () => {
  if (!userStore.isLogin) {
    alert('로그인 후 이용해주세요.')
    return
  }
  if (newComment.value.trim()) {
    await commentStore.createComment(threadId.value, newComment.value)
    newComment.value = ''
  } else {
    alert('댓글을 입력해주세요.')
  }
}

onMounted(() => {
  commentStore.fetchComments(threadId.value)
})

</script>

<style scoped>
.comment-list {
  /* max-width: 700px; */
  margin: 0 auto;
  padding: 1rem 0;
}
.login-warning {
  width: 100%;
  padding: 1rem;
  background-color: #f3ece8;
  color: #8a6d3b;
  border: 1px solid #e2cbb4;
  border-radius: 12px;
  text-align: center;
  font-size: 1rem;
}
.comment-form-inner {
  width: 100%;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.comment-form {
  display: flex;
  gap: 0.5rem;
  padding: 0.6rem;
  background-color: #d4cac2;
  border-radius: 12px;
  border: 1px solid #e2cbb4;
  margin-bottom: 1rem;
}

.comment-input {
  flex: 1;
  border: none;
  font-size: 1rem;
  padding: 0.5rem;
  outline: none;
  background: transparent;
  color: #3f2e1e;
}
.comment-input::placeholder {
  color: #a28c72;
}

.comment-button {
  background-color: #d96f32;
  color: white;
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}
.comment-button:hover {
  background-color: #ba5e2b;
}

.no-comment-text {
  text-align: center;
  color: #888;
  font-size: 0.95rem;
  margin-top: 2rem;
}

@media (max-width: 600px) {
  .comment-form {
    flex-direction: column;
  }
  .comment-button {
    width: 100%;
  }
}
</style>