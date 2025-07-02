<template>
  <button class="chatbot-button" @click="goToChatbot">
    <img src="@/assets/chatbot-icon.png" alt="챗봇" class="chatbot-icon" />
  </button>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goToChatbot = () => {
  router.push({ name: 'chat-bot' }) // 'ChatBot'은 router name
}
</script>

<style scoped>
.chatbot-button {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.chatbot-icon {
  width: 32px;
  height: 32px;
}
</style>
