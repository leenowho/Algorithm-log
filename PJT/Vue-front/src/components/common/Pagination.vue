<template>
  <div class="pagination">
    <button @click="emitGo(1)" :disabled="currentPage === 1">◀️◀️</button>
    <button @click="emitGo(currentPage - 1)" :disabled="currentPage === 1">◀️</button>

    <span v-if="startPage > 1">...</span>

    <button
      v-for="page in visiblePages"
      :key="page"
      @click="emitGo(page)"
      :class="{ active: page === currentPage }"
    >
      {{ page }}
    </button>

    <span v-if="endPage < totalPages">...</span>

    <button @click="emitGo(currentPage + 1)" :disabled="currentPage === totalPages">▶️</button>
    <button @click="emitGo(totalPages)" :disabled="currentPage === totalPages">▶️▶️</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  currentPage: Number,
  totalPages: Number
})
const emit = defineEmits(['go'])

const startPage = computed(() => Math.max(1, props.currentPage - 2))
const endPage = computed(() => Math.min(props.totalPages, props.currentPage + 2))

const visiblePages = computed(() => {
  const pages = []
  for (let i = startPage.value; i <= endPage.value; i++) {
    pages.push(i)
  }
  return pages
})

const emitGo = (page) => {
  if (page >= 1 && page <= props.totalPages) {
    emit('go', page)
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 2rem;
  margin-bottom: 1rem;
  gap: 0.4rem;
}

.pagination button {
  padding: 0.5rem 0.8rem;
  background-color: #f4e2d8;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  min-width: 36px;
}

.pagination button.active {
  background-color: #c88d66;
  color: white;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination span {
  padding: 0.5rem;
  color: #999;
}
</style>
