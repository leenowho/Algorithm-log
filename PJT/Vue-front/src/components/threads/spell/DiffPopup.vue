<template>
  <div class="popup-backdrop">
    <div class="popup-content">
      <h3>맞춤법 검사 결과</h3>
      <div class="diff-result">
        <span
          v-for="(part, index) in diff"
          :key="index"
          :class="{ add: part.added, remove: part.removed }"
        >
          {{ part.value }}
        </span>
      </div>

      <div class="actions">
        <button @click="$emit('confirm')">✅ 적용하기</button>
        <button @click="$emit('close')">❌ 닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ diff: Array })
defineEmits(['confirm', 'close'])
</script>

<style scoped>
.popup-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
.popup-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 80%;
  max-width: 600px;
  text-align: center;
}
.diff-result {
  margin: 1rem 0;
  font-size: 1.1rem;
  word-break: break-word;
}
.add {
  color: green;
  font-weight: bold;
}
.remove {
  color: red;
  text-decoration: line-through;
}
.actions button {
  margin: 0 0.5rem;
  padding: 0.5rem 1rem;
}
</style>
