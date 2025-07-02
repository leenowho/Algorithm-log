<template>
  <nav class="navbar">
    <div class="nav-container">
      <!-- 로고 -->
      <RouterLink :to="{ name: 'Main' }" class="brand-link">
        <img :src="logo" class="logo" />
        <span class="brand-name">책타래</span>
      </RouterLink>

      <!-- 데스크탑용 메뉴 -->
      <ul class="nav-links-desktop" v-show="isDesktop">
        <li><RouterLink :to="{ name: 'book-list' }">도서</RouterLink></li>
        <li><RouterLink :to="{ name: 'thread-list' }">Thread</RouterLink></li>
        <template v-if="userStore.isLogin">
          <li><RouterLink :to="{ name: 'user-profile' }">프로필</RouterLink></li>
          <li><a href="#" @click.prevent="onLogout">로그아웃</a></li>
        </template>
        <template v-else>
          <li><RouterLink :to="{ name: 'user-login' }">로그인</RouterLink></li>
          <li><RouterLink :to="{ name: 'user-signup' }">회원가입</RouterLink></li>
        </template>
      </ul>

      <!-- 햄버거 버튼 -->
      <div class="nav-toggle" v-show="!isDesktop" @click="isMenuOpen = !isMenuOpen">
        <span class="hamburger"></span>
        <span class="hamburger"></span>
        <span class="hamburger"></span>
      </div>
    </div>

    <!-- 모바일용 펼침 메뉴 -->
    <ul class="nav-links-mobile" v-show="!isDesktop && isMenuOpen">
      <li><RouterLink :to="{ name: 'book-list' }">도서</RouterLink></li>
      <li><RouterLink :to="{ name: 'thread-list' }">Thread</RouterLink></li>
      <template v-if="userStore.isLogin">
        <li><RouterLink :to="{ name: 'user-profile' }">프로필</RouterLink></li>
        <li><a href="#" @click.prevent="onLogout">로그아웃</a></li>
      </template>
      <template v-else>
        <li><RouterLink :to="{ name: 'user-login' }">로그인</RouterLink></li>
        <li><RouterLink :to="{ name: 'user-signup' }">회원가입</RouterLink></li>
      </template>
    </ul>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import logo from '@/assets/logo.png'

const isMenuOpen = ref(false)
const isDesktop = ref(window.innerWidth > 768)
const userStore = useUserStore()
const router = useRouter()

const onResize = () => {
  isDesktop.value = window.innerWidth > 768
  if (isDesktop.value) isMenuOpen.value = false
}
onMounted(() => window.addEventListener('resize', onResize))
onBeforeUnmount(() => window.removeEventListener('resize', onResize))

const onLogout = async () => {
  await router.push({ name: 'logout-info' })
  await userStore.logout()
}
</script>



<style scoped>
@font-face {
  font-family: 'SF_HambakSnow';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2106@1.1/SF_HambakSnow.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}

.navbar {
  background-color: #fff8f0;
  border-bottom: 1px solid #e3d5ca;
}

.nav-container {
  /* max-width: 1200px; */
  margin: 0 auto;
  padding: 0.8rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 로고 */
.brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  margin-left: 1.5rem;
}
.logo {
  width: 48px;
}
.brand-name {
  font-family: 'SF_HambakSnow', sans-serif;
  font-size: 1.8rem;
  color: #8b4513;
  margin-left: 0.6rem;
  margin-top: 5px;
}

/* 데스크탑 메뉴 */
.nav-links-desktop {
  display: flex;
  gap: 1rem;
  list-style: none;
}
.nav-links-desktop li a {
  color: #5a3e2b;
  font-weight: 600;
  text-decoration: none;
}
.nav-links-desktop li a:hover {
  color: #bf5d1f;
}

/* 햄버거 */
.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
}
.hamburger {
  width: 20px;
  height: 2px;
  background-color: #333;
}

/* 모바일 메뉴 */
.nav-links-mobile {
  display: flex;
  flex-direction: column;
  list-style: none;
  padding: 1rem 1.5rem;
  background-color: #fff8f0;
  border-top: 1px solid #e3d5ca;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04);
  gap: 0.75rem;
  align-items: end;
}

/* 모바일 메뉴 링크 스타일 */
.nav-links-mobile li a {
  text-decoration: none;
  color: #5a3e2b;
  font-weight: 600;
  font-size: 1rem;
  padding: 0.25rem 0;
  transition: color 0.3s ease;
}

.nav-links-mobile li a:hover {
  color: #bf5d1f;
}

/* 반응형 처리 */
@media (max-width: 768px) {
  .nav-links-desktop {
    display: none !important;
  }
  .nav-toggle {
    display: flex;
  }
}

</style>
