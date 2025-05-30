<template>
  <div class="chat-container">
    <div class="chat-history" ref="chatBox">
      <div
        v-for="(msg, index) in history"
        :key="index"
        :class="['chat-bubble', msg.sender === 'user' ? 'user' : 'bot']"
      >
        {{ msg.text }}
      </div>
      <div v-if="loading" class="chat-bubble bot typing-indicator">...</div>
      <div ref="scrollAnchor" />
    </div>

    <form class="chat-form" @submit.prevent="sendMessage">
      <input v-model="inputMessage" placeholder="메시지를 입력하세요" class="chat-input" />
      <button type="submit" class="chat-button">보내기</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const inputMessage = ref('')
const history = ref([])
const loading = ref(false)
const userStore = useUserStore()

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  const message = inputMessage.value
  inputMessage.value = ''

  // 사용자 메시지를 먼저 추가
  history.value.push({ sender: 'user', text: message })
  loading.value = true

  try {
    const res = await userStore.chatAi('post', message)
    console.log(res.history)
    const lastReply = res.history[res.history.length - 1]
    history.value.push({ sender: 'bot', text: lastReply.ai })
  } catch (err) {
    console.error('챗봇 오류:', err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const res = await userStore.chatAi('get')
    history.value = []

    for (const msg of res.history) {
      history.value.push({ sender: 'user', text: msg.user })
      history.value.push({ sender: 'bot', text: msg.ai })
    }
  } catch (err) {
    console.error('히스토리 로딩 실패:', err)
  }
})
</script>

<style scoped>
.chat-container {
  width: 100%;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chat-history {
  height: 500px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 1rem;
  background-color: #fffaf4;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.chat-bubble {
  max-width: 70%;
  margin: 0.5rem 0;
  padding: 0.75rem 1rem;
  border-radius: 18px;
  line-height: 1.4;
  word-wrap: break-word;
}

.chat-bubble.user {
  align-self: flex-end;
  background-color: #ffe4c4;
  color: #333;
  border-bottom-right-radius: 0;
}

.chat-bubble.bot {
  align-self: flex-start;
  background-color: #f3e0dc;
  color: #333;
  border-bottom-left-radius: 0;
}

.typing-indicator {
  font-style: italic;
  opacity: 0.6;
  animation: blink 1s steps(1) infinite;
}

@keyframes blink {
  0% { opacity: 0.2 }
  50% { opacity: 1 }
  100% { opacity: 0.2 }
}

.chat-form {
  display: flex;
  gap: 0.5rem;
}

.chat-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.chat-button {
  padding: 0.75rem 1.5rem;
  background-color: #b05e27; /* 가을 브라운 계열 */
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-button:hover {
  background-color: #924b1d;
}
</style>
