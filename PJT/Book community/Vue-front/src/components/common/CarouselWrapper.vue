<template>
  <div class="header-row">
    <h3 class="section-title">{{ title }}</h3>
    <RouterLink v-if="viewAllLink" :to="viewAllLink" class="view-all">전체 보기 ➝</RouterLink>
  </div>
  <div
    class="carousel-wrapper"
    @mouseenter="stopAutoSlide"
    @mouseleave="startAutoSlide"
  >
    <button @click="prev" :disabled="currentIndex === 0">◀</button>

    <div class="carousel-container" ref="container">
      <div
        class="carousel-track"
        :style="{
          width: `${items.length * itemWidth}px`,
          transform: `translateX(-${currentIndex * itemWidth}px)`
        }"
      >
        <div
          class="carousel-item"
          v-for="(item, i) in items"
          :key="i"
          :style="{ width: `${itemWidth}px` }"
        >
          <slot :item="item" />
        </div>
      </div>
    </div>

    <button @click="next" :disabled="currentIndex >= maxIndex">▶</button>
  </div>
  <div class="carousel-indicators">
    <span
      v-for="(item, i) in totalPages"
      :key="i"
      :class="{ active: i === currentPage }"
      @click="goToPage(i)"
    ></span>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  title: String,
  viewAllLink: Object,
  items: Array,
  autoSlide: {
    type: Boolean,
    default: true
  },
  slideInterval: {
    type: Number,
    default: 3000
  }
})

const currentIndex = ref(0)
const container = ref(null)
const itemWidth = ref(0)
const visibleCount = ref(1)
let intervalId = null

const maxIndex = computed(() =>
  props.items.length - visibleCount.value
)

const resize = () => {
  nextTick(() => {
    const width = container.value?.offsetWidth || 0
    if (width >= 1280) visibleCount.value = 5
    else if (width >= 1024) visibleCount.value = 4
    else if (width >= 768) visibleCount.value = 3
    else if (width >= 540) visibleCount.value = 2
    else visibleCount.value = 1

    itemWidth.value = width / visibleCount.value
  })
}

const next = () => {
  if (currentIndex.value < maxIndex.value) {
    currentIndex.value++
  } else {
    currentIndex.value = 0 // 다시 처음으로
  }
}

const prev = () => {
  if (currentIndex.value > 0) currentIndex.value--
}

const startAutoSlide = () => {
  if (props.autoSlide) {
    intervalId = setInterval(() => {
      next()
    }, props.slideInterval)
  }
}

const stopAutoSlide = () => {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}
const currentPage = computed(() =>
  Math.floor(currentIndex.value / visibleCount.value)
)

const totalPages = computed(() =>
  Math.ceil(props.items.length / visibleCount.value)
)

const goToPage = (page) => {
  currentIndex.value = page * visibleCount.value
}

onMounted(() => {
  resize()
  startAutoSlide()
  window.addEventListener('resize', resize)
})

onUnmounted(() => {
  stopAutoSlide()
  window.removeEventListener('resize', resize)
})
</script>


<style scoped>
.carousel-wrapper {
  display: flex;
  align-items: center;
  overflow: hidden;
}
.carousel-container {
  overflow: hidden;
  flex: 1;
}
.carousel-track {
  display: flex;
  transition: transform 1s ease;
}
.carousel-item {
  height: 100%; /* ✅ 높이 채우기 */
  display: flex;
  align-items: stretch;
}
button {
  border: none;
  background: transparent;
  font-size: 1.5rem;
  cursor: pointer;
}
button:disabled {
  opacity: 0.3;
}
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
.carousel-indicators {
  display: flex;
  justify-content: center;
  margin-top: 10px;
  gap: 6px;
}
.carousel-indicators span {
  width: 10px;
  height: 10px;
  background-color: #ddd;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s;
}
.carousel-indicators span.active {
  background-color: #a0522d;
}
</style>
