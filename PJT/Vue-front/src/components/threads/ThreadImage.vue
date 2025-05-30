<template>
  <img
    :src="currentSrc"
    :alt="alt"
    class="thread-cover"
  />
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  src: String,
  alt: String
})
const currentSrc = ref(props.src)

if (!currentSrc.value) {
  currentSrc.value = new URL('@/assets/default-thread.png', import.meta.url).href
}
</script>

<style scoped>
.thread-cover {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 12px;
}
</style>
