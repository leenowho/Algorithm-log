<!-- components/MainHeroBanner.vue -->
<template>
  <section class="hero-banner">
    <div class="overlay"></div> <!-- 배경 위에 덧씌울 투명 레이어 -->
    <div class="hero-content">
      <h1>
        {{ userStore.isLogin && userStore.userInfo ? `${userStore.userInfo.username}님, 마음을 채우는 책을 만나보세요` : '마음을 채우는 책을 만나다' }}
      </h1>
      <p>
        {{ userStore.isLogin ? '오늘도 당신의 취향을 기반으로 도서를 추천해드릴게요!' : '여러분의 취향을 기반으로 도서를 추천해주는 AI를 만나보세요!' }}
      </p>
      <RouterLink :to="{ name: 'book-list' }" class="explore-btn">지금 도서 탐색하기 ➝</RouterLink>
    </div>
  </section>
</template>


<script setup>
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
</script>

<style scoped>
.hero-banner {
  position: relative;
  background: url('/src/assets/banner.png') center/cover no-repeat;
  color: white;
  padding: 100px 20px;
  text-align: center;
  border-radius: 16px;
  margin-bottom: 2rem;
  overflow: hidden;
}

/* 배경 위 음영처리용 */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.171); /* 투명도 조절 */
  z-index: 1;
  border-radius: 16px;
}

/* 텍스트와 버튼은 z-index를 높여서 overlay 위로 */
.hero-content {
  position: relative;
  z-index: 2;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}
.explore-btn {
  display: inline-block;
  background-color: #C96F4A ;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
}
.explore-btn:hover {
  background-color: #9c4b2a;
}
</style>
