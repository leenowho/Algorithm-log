<template>
  <header class="thread-detail-header" v-if="thread">
    <h2 class="thread-title">{{ thread.title }}</h2>
    <RouterLink :to="{ name: 'thread-list' }" class="thread-link">목록으로</RouterLink>
  </header>
  <section class="thread-detail-layout">
    <!-- 📘 BookCard (좌측) -->
    <section class="thread-book-info" v-if="book">
      <img :src="book.cover_image" alt="cover" class="book-cover" />
      <div class="book-meta">
        <h3 class="book-title">{{ book.title }}</h3>
        <p class="book-author">저자: {{ book.author }}</p>
        <p class="book-category">카테고리: {{ book.category }}</p>
      </div>
    </section>

    <!-- 📋 Thread 내용 (우측) -->
    <div class="thread-column">

      <div class="clipboard">
        <div class="clip"></div>
        
        <article v-if="thread">
          <div class="thread-info">
            <img :src="imageUrl" class="top-image" />
            <div class="meta-info">
              <p>📅 {{ thread.read_date }} · 👤 {{ thread.user }}</p>
            </div>
            <p class="content">{{ thread.content }}</p>
          </div>

          <!-- 작성자만 수정/삭제/분석 가능 -->
          <div v-if="thread.user === userStore.userInfo?.username" class="thread-actions">
            <RouterLink :to="{ name: 'thread-update', params: { threadId: route.params.threadId } }" class="button-alike">
              ✏️ Thread 수정하기
            </RouterLink>
            <button @click="onDeleteThread" class="delete-button button-alike">🗑️ Thread 삭제하기</button>
            <button v-if="!thread?.summary && !loading" @click="analyzeThread" class="analyze-btn button-alike">
              감정 분석하기
            </button>
            <div v-if="thread?.summary" class="summary-box">
              🧠 감정 요약: "{{ thread.summary }}"
            </div>
          </div>

          <button class="like-button" @click="toggleLike">
            <span v-if="isLiked">💖</span>
            <span v-else>🤍</span>
            {{ likeCount }}
          </button>

          <div v-if="loading" class="overlay">
            <div class="loading-box">
              <img src="@/assets/loading.gif" alt="loading" />
              <p>당신의 Thread를 GPT가 읽고 분석 중입니다...</p>
            </div>
          </div>
        </article>

        <CommentList />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { useBookStore } from '@/stores/book'
import { useUserStore } from '@/stores/user'
import BookCard from '@/components/books/BookCard.vue'
import CommentList from '../comments/CommentList.vue'

const userStore = useUserStore()
const threadStore = useThreadStore()
const bookStore = useBookStore()
const route = useRoute()
const router = useRouter()

const threadId = route.params.threadId
const thread = ref(null)
const book = ref(null)
const loading = ref(false)

const imageUrl = computed(() => {
  if (thread.value?.thread_cover) {
    return `${threadStore.BASE_URL}${thread.value.thread_cover}?t=${Date.now()}`
  }
  return new URL('@/assets/default-thread.png', import.meta.url).href
})

const isLiked = computed(() => threadStore.likes[threadId]?.liked)
const likeCount = computed(() => threadStore.likes[threadId]?.like_count ?? thread.value?.like_count)

const fetchThread = async () => {
  try {
    const res = await threadStore.getThreadDetail(threadId)
    thread.value = res
    await bookStore.getBookDetailData(thread.value.book)
    book.value = bookStore.book
  } catch (err) {
    console.error(err)
  }
}

const toggleLike = async () => {
  if (!userStore.isLogin) {
    alert('로그인 후 이용해 주세요')
    return
  }
  try {
    await threadStore.toggleLike(threadId)
  } catch (err) {
    alert('좋아요 처리 중 오류가 발생했습니다.')
  }
}

const onDeleteThread = async () => {
  if (!confirm('정말로 이 Thread를 삭제하시겠습니까?')) return
  try {
    await threadStore.deleteThread(threadId)
    alert('Thread가 삭제되었습니다.')
    router.push({ name: 'thread-list' })
  } catch (err) {
    alert('삭제 중 오류가 발생했습니다.')
  }
}

const analyzeThread = async () => {
  loading.value = true
  try {
    await threadStore.getThreadSummary(thread.value.id)
    await fetchThread()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchThread)
</script>

<style scoped>
.thread-detail-header {
  position: relative;
  height: 60px;
  background-color: #fef9f5;
}

.thread-link {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background-color: #f4c28d;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
}

.thread-title {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  margin: 0;
  font-size: 1.5rem;
}

.thread-detail-layout {
  display: flex;
  flex-wrap: nowrap;
  gap: 2rem;
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
  align-items: flex-start;
}

.thread-column {
  flex: 1;
  min-width: 0;
}

.clipboard {
  background-color: #fffefc;
  border: 2px solid #bbb;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  position: relative;
}

.clip {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 24px;
  background: #999;
  border-radius: 8px 8px 0 0;
}

.top-image {
  margin: 0 auto;
  width: -webkit-fill-available;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: -80px;
  margin-bottom: 1rem;
  z-index: 1;
}

.thread-info {
  padding-top: 100px;
}

.thread-info h4 {
  font-size: 1.4rem;
  margin: 0.5rem 0;
}

.thread-info .content {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: #3f2e1e;
}

.thread-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}

a {
  padding: 0.5rem 1rem;
  background-color: #f2c29c;
  color: #fff;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.3s;
}
a:hover {
  background-color: #e0a677;
}

.button-alike {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 6px;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
  box-sizing: border-box;
}

.like-button {
  background-color: #ffccbc;
  color: #6e4e2e;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
  font-size: 1.1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.like-button:hover {
  background-color: #f7b199;
}

.delete-button {
  background-color: #f08080;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}
.delete-button:hover {
  background-color: #d65c5c;
}

.summary-box {
  margin-top: 16px;
  padding: 12px;
  background-color: #f0f9ff;
  border-left: 4px solid #38bdf8;
  font-style: italic;
  color: #0c4a6e;
}

.overlay {
  position: fixed;
  flex-direction: row;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-box {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 50%;
  max-width: 400px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.loading-box img {
  width: 120px;
  height: auto;
}

.analyze-btn {
  padding: 8px 16px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.analyze-btn:hover {
  background-color: #2563eb;
}
.analyze-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.thread-book-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background-color: #fffaf5;
  border-radius: 12px;
  padding: 1.2rem;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
  max-width: 260px;
}

.book-cover {
  width: 100%;
  aspect-ratio: 3/4;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}

.book-meta {
  flex: 1;
}

.book-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.book-author,
.book-category {
  font-size: 0.95rem;
  color: #5b4231;
}

@media (max-width: 974px) {
  .thread-detail-layout {
    flex-direction: column;
    align-items: center;
  }

  .thread-column {
    width: 100%;
  }
}

@media (max-width: 974px) {
  .thread-book-info {
    flex-direction: row;
    justify-content: center;
    align-items: flex-start;
    width: 100%;
    gap: 1rem;
    max-width: 100%;
    width: -webkit-fill-available;
  }
  .book-cover {
    width: 100px;
    aspect-ratio: 3 / 4;
    object-fit: cover;
    border-radius: 8px;
    flex-shrink: 0;
  }

  .book-meta {
    flex: 1;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.2rem;
  }
}

</style>
