<template>
  <section class="favorite-books">
    <h3>📚 찜한 도서 목록</h3>

    <div v-if="books.length === 0">찜한 도서가 없습니다.</div>

    <div class="book-list">
      <BookCard v-for="book in books" :key="book.id" :book="book" />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from "@/stores/book";
import BookCard from '@/components/books/BookCard.vue'
import axios from '@/plugins/axios'
const bookStore = useBookStore()

const books = ref([])


onMounted(async () => {
  books.value = await bookStore.getFavoriteBook()
})
</script>

<style scoped>
.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
}
</style>
