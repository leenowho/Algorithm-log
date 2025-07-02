<template>
  <div>
    <h1>Thread 수정</h1>
    <section class="thread-create-container" v-if="mounted">
      <!-- 상단에 BookCard 재활용 -->
      <BookCard :book="bookStore.book" class="book-preview" />
      <ThreadForm :initial-thread="thread" :book="bookStore.book"/>
      <!-- ThreadForm 컴포넌트 -->
    </section>
    <div v-else>
      <p>로딩 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useThreadStore } from "@/stores/thread"
import { useBookStore } from '@/stores/book'
import ThreadForm from "@/components/threads/ThreadForm.vue"
import BookCard from '@/components/books/BookCard.vue'

const route = useRoute()
const threadStore = useThreadStore()
const bookStore = useBookStore()
const thread = ref(null)
const mounted = ref(false)
// 마운트 될 때 이미 작성된 thread 정보를 기반으로 책 정보를 불러온다.
onMounted(async () => {
  const id = route.params.threadId
  thread.value = await threadStore.getThreadDetail(id)
  await bookStore.getBookDetailData(thread.value.book)
  mounted.value = true
})
</script>

<style scoped>
div > h2 {
  text-align: center;
}
.thread-create-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  display: flex;
  gap: 2rem;
}

.book-preview {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background-color: #f9f9f9;
}
</style>