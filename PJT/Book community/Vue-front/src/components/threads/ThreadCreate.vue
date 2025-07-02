<template>
  <div>
    <h2>독후감 작성 </h2>
    <section class="thread-create-container">
      <!-- 상단에 BookCard 재활용 -->
      <BookCard :book="bookStore.book" class="book-preview" />
  
      <!-- ThreadForm 컴포넌트 -->
      <ThreadForm :book="bookStore.book"/>
    </section>
  </div>

<section class="thread-guide-section">
  <h3>✍ 독후감 작성 가이드</h3>
  <ul>
    <li><strong>읽게 된 계기:</strong> 이 책을 고르게 된 이유나 기대했던 점은 무엇인가요?</li>
    <li><strong>줄거리 요약:</strong> 책의 주요 내용이나 핵심 사건을 간단히 정리해보세요.</li>
    <li><strong>인상 깊은 장면/문장:</strong> 마음에 남은 문장이나 장면은 무엇이었나요? 왜 인상 깊었는지 설명해보세요.</li>
    <li><strong>느낀 점과 생각:</strong> 책을 통해 새롭게 알게 된 점이나 감정의 변화가 있었나요?</li>
    <li><strong>자신의 경험과 연결:</strong> 책 속의 내용이 자신의 삶이나 가치관과 어떤 관련이 있었는지 떠올려보세요.</li>
    <li><strong>추천 여부:</strong> 이 책을 다른 사람에게 추천한다면, 어떤 사람에게 추천하고 싶은가요? 이유는?</li>
    <li><strong>기억하고 싶은 문장:</strong> 오래도록 마음에 남을 문장이 있다면 기록해보세요.</li>
  </ul>
</section>




</template>

<script setup>
import { ref, onMounted } from 'vue'
import ThreadForm from "@/components/threads/ThreadForm.vue"
import BookCard from '@/components/books/BookCard.vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookStore } from '@/stores/book'

const route = useRoute()

const bookStore = useBookStore()
// 마운트 될 때 책 정보를 갱신한다(create에서는 url에 booId가 존재)
onMounted(() => {
  bookStore.getBookDetailData(route.params.bookId)
})
</script>

<style scoped>
div > h2 {
  text-align: center;
  font-size: 1.8rem;
  color: #3e2d1d;
  margin-bottom: 2rem;
}

.thread-create-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem;
  display: flex;
  gap: 2rem;
  justify-content: center;
}

/*  반응형: 모바일에서는 세로 쌓기 */
@media (max-width: 768px) {
  .thread-create-container {
    flex-direction: column;
    padding: 2rem 1.2rem;
    align-items: center;
  }

  .book-preview,
  .thread-form-container {
    width: 100%;
  }
}

.book-preview {
  flex: 1;
  min-width: 280px;
  background-color: #fffefc;
  padding: 1rem;
  border: 1px solid #e4cdb8;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}

.thread-form-container {
  flex: 2;
  background-color: #fffefc;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  max-width: 100%;
}

.thread-guide-section {
  margin: 3rem auto;
  max-width: 1000px;
  background-color: #fff8f0;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  font-family: 'Gowun Batang', serif;
}

.thread-guide-section h3 {
  font-size: 1.4rem;
  font-weight: bold;
  color: #3e2d1d;
  margin-bottom: 1rem;
}

.thread-guide-section ul {
  list-style-type: '💡 ';
  padding-left: 1.2rem;
}

.thread-guide-section li {
  margin-bottom: 0.6rem;
  line-height: 1.6;
  color: #5a3b2e;
}

</style>