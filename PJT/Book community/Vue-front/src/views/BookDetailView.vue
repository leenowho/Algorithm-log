<template>
  <div class="book-detail-layout">
    <!-- 좌측: 유사도 도서 추천 -->
    <aside class="sidebar">
      <h3 class="sidebar-title">📚 유사한 도서</h3>
      <ul class="recommend-list">
        <li 
          v-for="book in bookStore.recommendedBooks" 
          :key="book.id" 
          class="recommend-card"
        >
          <RouterLink :to="{ name: 'book-detail', params: { bookId: book.id } }" class="card-link">
            <img v-if="book.cover_image" :src="book.cover_image" alt="book cover" class="recommend-img" />
            <div class="card-content">
              <strong class="card-title">{{ book.title }}</strong>
            </div>
          </RouterLink>
        </li>
      </ul>
    </aside>

    <!-- 중앙: 도서 상세 -->
    <div class="book-main">
      <!-- 이미지 -->
      <div class="book-image">
        <a :href="bookStore.book.aladin_link" target="_blank">
          <img :src="bookStore.book.cover_image" alt="book cover" class="book-cover-img" />
        </a>
      </div>

      <!-- 상세 정보 -->
      <div class="book-info">
        <h2 class="book-title">{{ bookStore.book.title }}</h2>
        <p class="book-author">✍️ {{ bookStore.book.author }}</p>
        <p class="book-pub">
          출판사: {{ bookStore.book.publisher || '정보 없음' }}<br />
          출판일: {{ bookStore.book.pub_date || '정보 없음' }}
        </p>
        <p class="book-desc">{{ bookStore.book.description || '설명 없음' }}</p>

        <!-- 버튼 영역 -->
        <div class="book-actions">
          <button @click="onToggleFavorite" class="like-btn">
            {{ isLiked ? '💖' : '🤍' }} {{ likeCount }}명 좋아요
          </button>
          <RouterLink
            :to="{ name: 'thread-create', params: { bookId: route.params.bookId } }"
            class="thread-btn">
            ✏️ 독후감 작성
          </RouterLink>
        </div>

        <!-- 지도 -->
        <div class="map-wrapper">
          <h3 class="section-subtitle">📌 근처 도서관</h3>
          <iframe
            v-if="mapUrl"
            :src="mapUrl"
            width="100%"
            height="300"
            class="map-frame"
            allowfullscreen
            loading="lazy"
          ></iframe>
        </div>

        <!-- 영상 -->
        <div class="youtube-wrapper">
          <h3 class="section-subtitle">🎥 관련 영상</h3>
          <template v-if="videoId">
            <iframe
              width="100%"
              height="315"
              :src="`https://www.youtube.com/embed/${videoId}`"
              frameborder="0"
              allowfullscreen
              class="youtube-frame"
            ></iframe>
          </template>
          <p v-else class="no-video-msg">🔍 관련 영상을 찾을 수 없습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useBookStore } from '@/stores/book'
import { useUserStore } from '@/stores/user'

const bookStore = useBookStore()
const userStore = useUserStore()
const route = useRoute()

const mapUrl = ref('')
const videoId = ref('')
const lastFetchedVideoId = ref(bookStore.book.id) // ✅ 마지막으로 fetch한 bookId 저장

const bookId = computed(() => Number(route.params.bookId))
const isLiked = computed(() => bookStore.favorites[bookId.value]?.favorited || false)
const likeCount = computed(() => bookStore.favorites[bookId.value]?.favorite_count || 0)

const onToggleFavorite = async () => {
  if (!userStore.isLogin) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const res = await bookStore.toggleFavorite(route.params.bookId)
  } catch (err) {
    alert('찜 처리 중 오류 발생')
    console.error(err)
  }
}


const fetchYouTubeVideo = async () => {
  const query = bookStore.book.title + ' 책 소개'
  try {
    const res = await bookStore.fetchYouTubeVideo(query)
    if (res.data.videoId) {
      videoId.value = res.data.videoId
    } else {
      videoId.value = null
    }
  } catch (err) {
    // console.error('❌ 유튜브 영상 불러오기 실패:', err)
  }
}

// ✅ 책 데이터 호출
const fetchBookData = async () => {
  await bookStore.getBookDetailData(bookId.value)
  await bookStore.getRecommendedBooks(bookId.value)
  updateMapToCurrentLocation()

  // ✅ 유튜브 API는 bookId가 이전과 다를 때만 호출
  if (lastFetchedVideoId.value !== bookId.value) {
    // console.log('🎥 유튜브 API 호출: bookId 바뀜 →', bookId.value)
    lastFetchedVideoId.value = bookId.value
    await fetchYouTubeVideo()
  } else {
    // console.log('⛔ 유튜브 API 호출 생략 (중복 bookId)', bookId.value)
  }
}

// ✅ 위치 기반 지도 url 생성
const updateMapToCurrentLocation = () => {
  if (!navigator.geolocation) return
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const { latitude, longitude } = pos.coords
      mapUrl.value = `https://www.google.com/maps?output=embed&q=도서관&ll=${latitude},${longitude}&z=14`
    },
    // (err) => console.error('위치 정보 실패:', err)
  )
}

// ✅ 최초 마운트 + 경로 변경 시 데이터 재요청
onMounted(fetchBookData)
watch(() => route.params.bookId, fetchBookData)

</script>


<style scoped>
.book-detail-layout {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  max-width: 1400px;
  margin: 4rem auto;
  padding: 0 2rem;
}

/* 유사도 추천 도서 */
.sidebar {
  flex: 1 1 250px;
  order: 1;
}

.sidebar-title {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #3e2d1d;
}

.recommend-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recommend-card {
  background-color: #fffaf5;
  border: 1px solid #e4cdb8;
  border-radius: 12px;
  transition: transform 0.2s;
}
.recommend-card:hover {
  transform: translateY(-2px);
}

.card-link {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
}

.recommend-img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-bottom: 1px solid #e4cdb8;
}

.card-content {
  padding: 0.7rem 1rem;
}

.card-title {
  font-size: 1rem;
  font-weight: bold;
  color: #3e2d1d;
}

/* 중앙 도서 정보 */
.book-main {
  flex: 3 1 700px;
  background-color: #fffefb;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.06);
  font-family: 'Gowun Batang', serif;
  order: 2;
}

.book-image {
  text-align: center;
  margin-bottom: 1.5rem;
}

.book-cover-img {
  width: 240px;
  border-radius: 12px;
  border: 2px solid #e0d3c2;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.book-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.4rem;
  color: #3d2b1f;
}

.book-author,
.book-pub {
  font-size: 1rem;
  color: #6e4b3a;
  margin-bottom: 0.6rem;
}

.book-desc {
  margin: 1rem 0 2rem;
  color: #4b372c;
  line-height: 1.7;
}

.book-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.like-btn,
.thread-btn {
  padding: 0.6rem 1.4rem;
  font-weight: bold;
  border-radius: 8px;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  box-sizing: border-box;
}

.like-btn {
  background-color: #fff0e6;
  color: #b37442;
  border: 1px solid #dcbfa9;
}

.thread-btn {
  background-color: #b37442;
  color: white;
  text-decoration: none;
}

.thread-btn:hover {
  background-color: #965a2d;
}

.section-subtitle {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 2rem 0 1rem;
  color: #3e2d1d;
}

.map-frame,
.youtube-frame {
  border: none;
  border-radius: 12px;
}

/* ✅ 반응형 설정 */
/* 중간 이하 화면: 유사 도서 하단으로 이동 */
@media (max-width: 1130px) {
  .book-detail-layout {
    flex-direction: column;
    padding: 0, 1rem;
  }

  .sidebar {
    order: 3;
    width: 100%;
    margin-top: 2rem;
  }

  .book-main {
    order: 1;
    /* width: 95%; */
  }

  .book-actions {
    flex-direction: column;
  }

  .like-btn,
  .thread-btn {
    width: 100%;
  }
}
.no-video-msg {
  color: #6e4b3a;
  font-style: italic;
  background-color: #fff4ee;
  padding: 1rem;
  border-radius: 10px;
  border: 1px dashed #d6b49c;
  margin-top: 0.5rem;
  text-align: center;
}
</style>
