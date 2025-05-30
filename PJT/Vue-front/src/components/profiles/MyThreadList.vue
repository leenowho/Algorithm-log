<template>
  <section class="my-threads">
    <h3>📝 내가 작성한 쓰레드</h3>

    <div v-if="myThreads.length === 0">작성한 쓰레드가 없습니다.</div>

    <div class="thread-list">
      <ThreadCard v-for="thread in myThreads" :key="thread.id" :thread="thread" />
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useThreadStore } from '@/stores/thread'
import { useUserStore } from '@/stores/user'
import ThreadCard from '@/components/threads/ThreadCard.vue'

const threadStore = useThreadStore()
const userStore = useUserStore()

// 작성자 필터링
const myThreads = computed(() =>
  threadStore.threadList.filter(
    thread => thread.user === userStore.userInfo.username
  )
)
</script>

<style scoped>
.thread-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
</style>
