<template>
  <div @click="goToDetail" class="book-card" :class="{ compact: size === 'compact' }">
    <!-- ❤️ 찜 버튼 -->
    <button class="favorite-btn" @click.stop="toggleFavorite">
      <span v-if="favorited">❤️</span>
      <span v-else>🤍</span>
      {{ favoriteCount }}
    </button>

    <img :src="book.cover_image" alt="book cover" class="book-img" />

    <h3 class="book-title">{{ book.title }}</h3>
    <p class="book-author">저자: {{ book.author }}</p>
    <p class="book-category">카테고리: {{ book.category }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useBookStore } from '@/stores/book'

const props = defineProps({
  book: Object,
  size: {
    type: String,
    default: 'default' // 'default' | 'compact'
  }
})

const router = useRouter()
const userStore = useUserStore()
const bookStore = useBookStore()

const favorited = computed(() => {
  return bookStore.favorites[props.book.id]?.favorited ?? false
})
// ref(bookStore.favorites[props.book.id]?.favorited ?? false)
const favoriteCount = computed(() => {
  return bookStore.favorites[props.book.id]?.favorite_count ?? 0
})
// ref(bookStore.favorites[props.book.id]?.favorite_count ?? 0)

const goToDetail = () => {
  router.push({ name: 'book-detail', params: { bookId: props.book.id } })
}

const toggleFavorite = async () => {
  if (!userStore.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const res = await bookStore.toggleFavorite(props.book.id)
    favorited.value = res.favorited
    favoriteCount.value = res.favorite_count
  } catch (err) {
    alert('찜 처리 중 오류 발생')
    console.error(err)
  }
}
</script>

<style scoped>
.book-card {
  position: relative;
  width: 100%;
  max-width: 220px;
  background-color: #f7e4d4;
  border-radius: 12px;
  box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1rem;
  text-align: center;
  transition: transform 0.2s ease;
  cursor: pointer;
  box-sizing: border-box;
}

.book-card.compact {
  max-width: 300px;
  padding: 1.25rem;
  font-size: 1.05rem;
}
.book-card:hover {
  transform: translateY(-4px);
}
.book-img {
  width: 100%;
  aspect-ratio: 3 / 4;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.75rem;
}

/* 텍스트 정리 */
.book-title,
.book-author,
.book-category {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-title {
  font-size: 1rem;
  font-weight: 600;
  color: #3e2d1d;
  margin-bottom: 0.3rem;
}

.book-author,
.book-category {
  font-size: 0.85rem;
  color: #6e4b3a;
}

/* 찜 버튼 */
.favorite-btn {
  position: absolute;
  top: 8px;
  right: 12px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 999px;
  padding: 4px 8px;
  font-size: 0.9rem;
  color: #d94f4f;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: background-color 0.2s ease;
  z-index: 10;
}
.favorite-btn:hover {
  background-color: #f8e4e4;
}
.favorite-btn span:last-child {
  font-size: 0.75rem;
  margin-left: 4px;
}
</style>
