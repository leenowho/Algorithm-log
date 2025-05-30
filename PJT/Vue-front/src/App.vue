<template>
  <div class="app">
    <NavBar />
    <RouterView />
    <!-- <ChatBot v-if="userStore.isLogin"/> -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBookStore } from "@/stores/book"
import { useUserStore } from '@/stores/user'
import { setAuthInterceptor } from '@/plugins/axios'
import { useThreadStore } from './stores/thread'
import NavBar from "@/components/NavBar.vue"
import ChatBot from "@/components/ChatBotButton.vue"
import Footer from './components/Footer.vue'

const userStore = useUserStore()
const bookStore = useBookStore()
const threadStore = useThreadStore()

if (userStore.accessToken) {
  setAuthInterceptor(userStore.accessToken)  // ✅ 토큰을 axios에 재주입
}

onMounted(() => {
  bookStore.fetchBooks()
  bookStore.getCategoryData()
  threadStore.getThreadList()
})
</script>

<style scoped>


.app {
  min-height: 100vh; /* 화면 전체 높이 */
  background-color: #fff9f3; /* 따뜻한 베이지 계열 */
  color: #4e3d2e; /* 브라운 텍스트 */
  font-family: 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
  display: flex;
  flex-direction: column;
}

/* 모든 RouterView가 자연스럽게 아래로 배치되도록 */
RouterView {
  flex-grow: 1;
  padding: 1.5rem;
  box-sizing: border-box;
}

</style>

<style>
html, body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>