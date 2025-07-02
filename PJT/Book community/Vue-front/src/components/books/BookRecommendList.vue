<template>
  <div class="recommend-list">
    <h2 class="page-title">📚 관심 분야 기반 추천 도서</h2>

    <div v-if="books.length" class="book-grid">
      <BookCard v-for="book in books" :key="book.id" :book="book" />
    </div>

    <p v-else class="empty-msg">추천 도서가 아직 없습니다. 관심 분야를 선택해보세요!</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/book'
import BookCard from '@/components/books/BookCard.vue'

const bookStore = useBookStore()
const books = ref([])

const fetchRecommendedBooks = async () => {
  try {
    const res = await bookStore.fetchUserRecommendedBooks()
    books.value = res.data
  } catch (err) {
    console.error('추천 도서 전체 보기 실패:', err)
  }
}

onMounted(async () => {
  await fetchRecommendedBooks()
})
</script>

<style scoped>
.recommend-list {
  padding: 2rem;
  background-color: #fffdf9;
}
.page-title {
  font-size: 1.5rem;
  color: #5a3b2e;
  margin-bottom: 1rem;
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}
.empty-msg {
  color: #777;
  margin-top: 2rem;
  text-align: center;
}
</style>
