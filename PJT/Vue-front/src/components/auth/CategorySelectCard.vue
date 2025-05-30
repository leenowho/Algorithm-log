<!-- components/CategorySelectCard.vue -->
<template>
  <div class="category-select-wrapper">
    <h3 class="select-title">관심 분야를 선택하세요</h3>
    <div class="category-grid">
      <div
        v-for="category in categories"
        :key="category.id"
        :class="['category-card', selected.includes(category.id) ? 'selected' : '']"
        @click="toggleCategory(category.id)"
      >
        {{ category.name }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue'

const props = defineProps({
  categories: Array,
  modelValue: Array,  // v-model: selected category ids
})
const emit = defineEmits(['update:modelValue'])

const selected = ref([...props.modelValue || []])

watch(() => props.modelValue, (val) => {
  selected.value = [...val]
})

const toggleCategory = (id) => {
  if (selected.value.includes(id)) {
    selected.value = selected.value.filter((c) => c !== id)
  } else {
    selected.value.push(id)
  }
  emit('update:modelValue', selected.value)
}
</script>

<style scoped>
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.category-card {
  padding: 1rem 0.5rem;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 12px;
  cursor: pointer;
  background-color: #fff;
  transition: 0.2s;
}

.category-card:hover {
  background-color: #f7eee5;
}

.category-card.selected {
  background-color: #ffe7cc;
  border-color: #e09562;
  font-weight: bold;
}
</style>