<template>
  <div class="thread-list-container">
    <h2 class="title">📚 사용자 스레드 목록</h2>
    <div class="thread-grid">
      <ThreadCard 
        v-for="thread in threadStore.threadList"
        :key="thread.id"
        :thread="thread"
      />
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useThreadStore } from "@/stores/thread"
import ThreadCard from "@/components/threads/ThreadCard.vue"

const threadStore = useThreadStore()

</script>
<style scoped>
.thread-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.title {
  text-align: center;
  margin-bottom: 2rem;
  color: #704214;
}

/* 반응형 그리드 */
.thread-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(1, 1fr); /* 기본: 1개 */
}

@media (min-width: 768px) {
  .thread-grid {
    grid-template-columns: repeat(3, 1fr); /* 중간 화면: 3개 */
  }
}
@media (min-width: 1200px) {
  .thread-grid {
    grid-template-columns: repeat(4, 1fr); /* 큰 화면: 4개 */
  }
}
</style>
