<template>
  <CarouselWrapper title="📚 베스트 셀러" :viewAllLink="{ name: 'book-list' }" :items="books">
    <template #default="{ item }">
      <BookCard :book="item" />
    </template>
  </CarouselWrapper>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from '@/stores/book'
import CarouselWrapper from '@/components/common/CarouselWrapper.vue'
import BookCard from '@/components/books/BookCard.vue'

const books = ref([])
const bookStore = useBookStore()

onMounted(async () => {
  books.value = await bookStore.fetchBannerBooks()
})
</script>
