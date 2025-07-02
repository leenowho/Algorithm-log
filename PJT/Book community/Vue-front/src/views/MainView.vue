<template>
  <div class="main-container">
    <!-- 베너도 컴포넌트로 분리 -->
    <!-- <div class="banner">
      <img :src="banner" alt="">
      <h1>마음을 채우는 책을 만나다</h1>
      <p>여러분의 취향을 기반으로 도서를 추천해주는 AI를 만나보세요!</p>
    </div> -->


    <MainHeroBanner />
    <!-- <h2 v-if="userStore.accessToken">{{ userStore.userInfo.username }}님 환영합니다!</h2> -->
    <div v-if="userStore.isLogin">
      <RecommendBookSlider />
    </div>
    <!-- 도서 목록은 슬라이딩 윈도우를 적용 -->
    <div>
      <!-- 사용자가 전체 보기를 누르면 그때 BookList를 보여준다. -->
      <BookBannerSlider />
    </div>
    <!-- 쓰레드 10개만 슬라이딩 윈도우를 적용 -->
    <div>
      <ThreadBannerSlider />
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useBookStore } from '@/stores/book'
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BookBannerSlider from "@/components/books/BookBannerSlider.vue"
import ThreadBannerSlider from "@/components/threads/ThreadBannerSlider.vue"
import MainHeroBanner from '@/components/MainHeroBanner.vue'
import RecommendBookSlider from '@/components/books/RecommendBookSlider.vue'


import banner from "@/assets/banner.png";

const userStore = useUserStore()
const bookStore = useBookStore()
const router = useRouter()

</script>

<style scoped>
.main-container {
  background-color: #fff9f3;
  padding: 2rem;
  font-family: 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
  color: #4e3d2e;
}

.banner {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 수직 정렬 */
  align-items: center;     /* 수평 정렬 */
  text-align: center;
  height: 300px;
  border-radius: 12px;
  overflow: hidden;
  background-color: #000;
}
.banner img {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.6;
  z-index: 0;
}
.banner h1, .banner p {
  z-index: 1;
  background-color: rgba(255, 240, 220, 0.8);
  margin: 0.5rem 1rem;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  max-width: 90%;
  word-break: keep-all;
}

.banner h1 {
  font-size: 2rem;
  color: #5a3e2b;
}
.banner p {
  font-size: 1rem;
  color: #6e4c3c;
}

/* 사용자 환영 메시지 */
h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #7d4f36;
}

/* 슬라이더 영역 공통 스타일 */
div > div {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #fff4e8;
  border-radius: 12px;
  box-shadow: 0 0 8px rgba(150, 100, 50, 0.1);
}

/* 전체 보기 링크 */
a {
  margin-left: 1rem;
  text-decoration: none;
  color: #a0603d;
  font-weight: bold;
}
a:hover {
  color: #d68042;
}
</style>