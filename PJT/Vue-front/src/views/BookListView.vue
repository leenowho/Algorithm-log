<template>
  <div class="book-list-page">
    <!-- 🔍 검색창 + 필터 전체 영역 -->
    <div class="book-filter-bar">
      <!-- 햄버거 버튼 (모바일용) -->
      <button class="hamburger-toggle" @click="isFilterVisible = !isFilterVisible">
        ☰ 필터
      </button>

      <div class="filter-inner" :class="{ open: isFilterVisible }">
        <!-- 검색창 -->
        <input
          v-model="searchQuery"
          @input="onSearch"
          placeholder="제목, 작가, 설명으로 검색"
          class="search-bar"
        />

        <!-- 카테고리 버튼 -->
        <div class="category-filter">
          <button
            :class="{ active: selectedCategory === '' }"
            @click="filterByCategory('')"
          >
            전체
          </button>
          <button
            v-for="cate in bookStore.categories"
            :key="cate.id"
            :class="{ active: selectedCategory === cate.name }"
            @click="filterByCategory(cate.name)"
          >
            {{ cate.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- 📚 도서 목록 -->
    <div class="book-grid">
      <BookCard v-for="book in bookStore.books" :key="book.id" :book="book" />
    </div>

    <!-- 페이지네이션 -->
    <Pagination :currentPage="currentPage" :totalPages="bookStore.totalPages" @go="goToPage" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import debounce from 'lodash/debounce'
import BookCard from '@/components/books/BookCard.vue'
import Pagination from '@/components/common/Pagination.vue'
import { useBookStore } from '@/stores/book'

const bookStore = useBookStore()
const searchQuery = ref('')
const selectedCategory = ref('')
const currentPage = ref(1)
const isFilterVisible = ref(true) // 햄버거용 필터 토글 상태

const goToPage = async (page) => {
  currentPage.value = page
  await bookStore.fetchBooks(page, searchQuery.value, selectedCategory.value)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const debouncedSearch = debounce(async () => {
  currentPage.value = 1
  await bookStore.fetchBooks(1, searchQuery.value, selectedCategory.value)
}, 400)

const onSearch = () => {
  debouncedSearch()
}

const filterByCategory = async (category) => {
  selectedCategory.value = category
  currentPage.value = 1
  await bookStore.fetchBooks(1, searchQuery.value, selectedCategory.value)
}

onMounted(() => {
  bookStore.getCategoryData()
  bookStore.fetchBooks(1)
})
</script>

<style scoped>
.book-filter-bar {
  position: sticky;
  top: 0;
  z-index: 11;
  background-color: #fff8f0;
  padding: 1rem 1.2rem;
  border-bottom: 1px solid #e3d5ca;
}

.search-bar {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  margin-bottom: 1rem;
}

/* 카테고리 버튼을 그리드로 같은 폭 정렬 */
.category-filter {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 0.5rem;
}

/* 버튼 스타일 */
.category-filter button {
  padding: 0.5rem;
  background-color: #f8e9dd;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
}
.category-filter button.active {
  background-color: #c88d66;
  color: white;
}

/* 햄버거 버튼 기본 숨김 */
.hamburger-toggle {
  display: none;
  background: #eaa87d;
  color: white;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  margin-bottom: 0.8rem;
}

/* 모바일 전용: 햄버거 버튼 표시 + 토글 동작 */
@media (max-width: 768px) {
  .hamburger-toggle {
    display: inline-block;
  }

  .filter-inner {
    display: none;
    flex-direction: column;
    gap: 1rem;
  }

  .filter-inner.open {
    display: flex;
  }
}


/* 도서 카드 그리드 */
.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1.5rem;
  padding: 1rem 1.2rem;
}
</style>
