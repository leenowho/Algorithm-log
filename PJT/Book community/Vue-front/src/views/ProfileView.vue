<template>
  <section class="profile-container">
    <h2>내 프로필</h2>

    <!-- 👤 기본 정보 -->
    <div class="user-info">
      <p>👤 사용자명: {{ userStore.userInfo.username }}</p>
      <!-- <p>📧 이메일: {{ userStore.userInfo.email || '입력되지 않음' }}</p> -->
      <p>🧓 나이: {{ userStore.userInfo.age || '입력되지 않음' }}</p>
      <p>📛 이름: {{ userStore.userInfo.last_name || '' }}{{ userStore.userInfo.first_name || '' }}</p>
      <p class="category-label-title">🎯 관심 분야:</p>
      <div class="category-label-container">
        <template v-if="userStore.userInfo.interested_categories?.length">
          <span
            class="category-label"
            v-for="(name, idx) in categoryNames"
            :key="idx"
          >
            {{ name }}
          </span>
        </template>
        <span v-else class="category-label-empty">입력되지 않음</span>
      </div>

      <RouterLink :to="{ name: 'user-edit' }" class="edit-button">
        회원 정보 수정
      </RouterLink>
    </div>
    
    <hr />
    <h2>🗓 내 Thread 활동</h2>
    <CalendarHeatmap />
    <hr />

    <!-- 📚 찜한 책 -->
    <section class="profile-section">
      
      <template v-if="favoriteBooks.length">
        <CarouselWrapper
          title="📚 찜한 책"
          :items="favoriteBooks"
          :viewAllLink="{ name: 'user-favorite-books' }"
        >
          <template #default="{ item }">
            <BookCard :book="item" />
          </template>
        </CarouselWrapper>
      </template>
      <div v-else>
        <h3 class="carousel-title">📚 찜한 책</h3>
        <p class="empty-message">아직 찜한 책이 없습니다.</p>
      </div>
    </section>

    <hr />

    <!-- 📝 내가 작성한 Thread -->
    <section class="profile-section">
      
      <template v-if="myThreads.length">
        <CarouselWrapper
          title="✍️ 내가 작성한 Thread"
          :items="myThreads"
          :viewAllLink="{ name: 'user-threads' }"
        >
          <template #default="{ item }">
            <ThreadCard :thread="item" />
          </template>
        </CarouselWrapper>
      </template>
      <div v-else>
        <h3 class="carousel-title">✍️ 내가 작성한 Thread</h3>
        <p class="empty-message">아직 작성한 thread가 없습니다.</p>
      </div>
    </section>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useBookStore } from '@/stores/book'
import { useThreadStore } from '@/stores/thread'
import ThreadCard from '@/components/threads/ThreadCard.vue'

import CalendarHeatmap from '@/components/profiles/CalenderHeatmap.vue'
import CarouselWrapper from '@/components/common/CarouselWrapper.vue'
import BookCard from '@/components/books/BookCard.vue'

const bookStore = useBookStore()
const threadStore = useThreadStore()
const userStore = useUserStore()
const categoryList = ref(bookStore.categories)

// 작성자 필터링
const myThreads = computed(() => {
  return threadStore.threadList.filter(
    thread => thread.user === userStore.userInfo.username
  )}
)

const favoriteBooks = computed(() => {
  return bookStore.userFavoriteBookList
})

const categoryNames = computed(() => {
  const selected = userStore.userInfo.interested_categories || []
  return categoryList.value.filter(c => selected.includes(c.id)).map(c => c.name)
})
onMounted(async () => {
  await bookStore.getFavoriteBook()
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}
.user-info {
  background: #fdf7f3;
  padding: 1rem;
  border-radius: 10px;
}
hr {
  margin: 2rem 0;
}

.category-label-title {
  font-weight: bold;
  margin-bottom: 0.4rem;
  color: #6b4226;
}

.category-label-container {
  display: flex;
  flex-wrap: wrap; /* ✅ 여러 줄 허용 */
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.category-label {
  background-color: #f3e9dc;
  color: #5a3e2b;
  padding: 0.4rem 0.9rem;
  border-radius: 9999px; /* ✅ pill 모양 */
  font-size: 0.85rem;
  border: 1px solid #d6c6b9;
}

.category-label-empty {
  color: #aaa;
  font-size: 0.85rem;
}
.edit-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #eaa87d;
  color: white;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.3s;
  margin-top: 1rem;
}

.edit-button:hover {
  background-color: #d48960;
}
.profile-section {
  margin-bottom: 2rem;
}

.carousel-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 0.6rem;
  color: #6b4226;
  padding-left: 0.2rem;
}

.empty-message {
  color: #999;
  font-style: italic;
  text-align: center;
  margin: 1rem 0;
  font-size: 0.95rem;
}


</style>
