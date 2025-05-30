<template>
  <div class="thread-popup" v-if="open">
    <h3 class="thread-popup-title">📌 {{ date }}의 Thread</h3>

    <ul v-if="threads.length" class="thread-popup-list">
      <li
        v-for="thread in threads"
        :key="thread.id"
        class="thread-item"
        @click="$router.push(`/threads/${thread.id}`)"
      >
        <div class="thread-title">{{ thread.title }}</div>
        <div class="thread-user">작성자: {{ thread.user }}</div>
      </li>
    </ul>

    <p v-else class="thread-empty">작성된 Thread가 없습니다.</p>

    <div class="thread-close">
      <button @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  open: Boolean,
  date: String,
  threads: Array,
})
defineEmits(['close'])
</script>

<style scoped>
.thread-popup {
  position: fixed;               /* ✅ 화면 전체 기준 */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* ✅ 화면 정중앙 위치 */
  width: 360px;
  max-height: 80vh;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}
.thread-popup-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
}
.thread-popup-list {
  max-height: 250px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  margin: 0;
}
.thread-item {
  padding: 8px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}
.thread-item:hover {
  background-color: #f8f8f8;
}
.thread-title {
  font-weight: 500;
}
.thread-user {
  font-size: 12px;
  color: #666;
}
.thread-empty {
  font-size: 14px;
  color: #999;
}
.thread-close {
  text-align: right;
  margin-top: 12px;
}
</style>