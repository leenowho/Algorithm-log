<template>
  <CarouselWrapper title="🔥 인기 쓰레드" :viewAllLink="{ name: 'thread-list' }" :items="threads">
    <template #default="{ item }">
      <ThreadCard :thread="item" />
    </template>
  </CarouselWrapper>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useThreadStore } from '@/stores/thread'
import ThreadCard from '@/components/threads/ThreadCard.vue'
import CarouselWrapper from '@/components/common/CarouselWrapper.vue'

const threads = ref([])
const threadStore = useThreadStore()

onMounted(async () => {
  threads.value = await threadStore.getHotThreads()
})
</script>

<style>
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.view-all {
  font-size: 0.9rem;
  color: #a0522d;
  text-decoration: none;
  font-weight: 500;
}
.view-all:hover {
  text-decoration: underline;
}
</style>