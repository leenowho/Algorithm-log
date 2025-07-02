<template>
  <div v-if="recommendedBooks">
    <CarouselWrapper
      title="관심 분야 추천 도서"
      :items="recommendedBooks"
      :viewAllLink="{ name: 'book-recommend-list' }"
    >
      <template #default="{ item }">
        <div class="carousel-item book-card">
          <BookCard :book="item" />
        </div>
      </template>
    </CarouselWrapper>
  </div>
  <p v-else class="empty-msg">추천 도서가 아직 없습니다.</p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CarouselWrapper from '@/components/common/CarouselWrapper.vue'
import BookCard from '@/components/books/BookCard.vue'
import { useBookStore } from '@/stores/book'

const bookStore = useBookStore()
const recommendedBooks = ref([])

const fetchRecommendedBooks = async () => {
  try {
    const res = await bookStore.fetchUserRecommendedBooks()
    recommendedBooks.value = res.data
  } catch (err) {
    console.error('추천 도서 불러오기 실패:', err)
    recommendedBooks.value = []
  }
}

onMounted(async () => {
  await fetchRecommendedBooks()
})
</script>

<style scoped>
.empty-msg {
  color: #888;
  font-size: 0.95rem;
  margin: 1rem 0;
}
</style>
