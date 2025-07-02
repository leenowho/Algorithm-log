<template>
  <div class="thread-card" @click="onThreadDetail" v-if="thread">
    <div class="image-wrapper">
      <img :src="imageUrl" @error="onImageError" alt="Thread Cover" />
      <button class="like-button" @click.stop="toggleLike">
        <span v-if="isLiked">💖</span>
        <span v-else>🤍</span>
        {{ likeCount }}
      </button>
    </div>
    <div class="thread-info">
      <h4>
        {{ thread.title.length >= 10 ? thread.title.slice(0, 10) + '...' : thread.title }}
      </h4>
      <p>{{ thread.user }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from "vue-router"
import { useUserStore } from '@/stores/user'
import { useThreadStore } from "@/stores/thread"
const router = useRouter()
const threadStore = useThreadStore()
const userStore = useUserStore()
const props = defineProps({
  thread: Object
})
const isLiked = computed(() => threadStore.likes[props.thread.id]?.liked ?? false)
const likeCount = computed(() => threadStore.likes[props.thread.id]?.like_count ?? props.thread.like_count)

const imageUrl = ref(`${props.thread.thread_cover}`)
const onImageError = () => {
  imageUrl.value = new URL('@/assets/default-thread.png', import.meta.url).href
}

const onThreadDetail = function () {
  router.push({ name: 'thread-detail', params: { threadId: props.thread.id } })
}

const toggleLike = async () => {
  if (!userStore.isLogin) {
    alert('로그인 후 이용해주세요.')
    return
  }
  try {
    await threadStore.toggleLike(props.thread.id)
  } catch (err) {
    alert('좋아요 처리 중 오류가 발생했습니다.')
  }
}
</script>

<style scoped>
.thread-card {
  display: flex;
  flex-direction: column;
  background-color: #fdf6f0;
  border: 1px solid #e6ccb2;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s ease-in-out;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  height: 100%;
}
.thread-card:hover {
  transform: scale(1.03);
}
.image-wrapper {
  position: relative;
  width: 100%;
}
.thread-card img {
  width: 100%;
  aspect-ratio: 1 / 1; /* 1024x1024 비율 유지 */
  object-fit: cover;
  background-color: #fff;
}
.thread-info {
  padding: 12px;
}
.thread-info h4 {
  margin: 0;
  color: #8b4513;
}
.thread-info p {
  color: #a0522d;
  font-size: 0.9rem;
  margin-top: 4px;
}
.thread-like button {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}
.like-button {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 1rem;
  color: #8b0000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.like-button:hover {
  background-color: #ffe2db;
}
</style>