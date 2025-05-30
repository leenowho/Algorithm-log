<template>
  <div class="thread-form-container">
    <form class="thread-form" @submit.prevent="onAddThread">
      <div class="form-group">
        <label for="title" class="form-label">제목</label>
        <input type="text" id="title" v-model="title" class="form-input">
      </div>

      <div class="form-group">
        <label for="content" class="form-label">내용</label>
        <textarea id="content" rows="10" cols="50" v-model="content" class="form-textarea"></textarea>
      </div>

      <div class="form-group">
        <label for="read-date" class="form-label">읽은 날</label>
        <input type="date" id="read-date" v-model="read_date" class="form-input">
      </div>

      <button class="submit-btn">작성하기</button>
    </form>

    <button class="spellcheck-btn" @click="runSpellCheck">맞춤법 검사</button>

    <!-- 로딩 gif 오버레이 -->
    <div v-if="loading" class="overlay">
      <div class="loading-box">
        <img src="@/assets/loading.gif" alt="loading" />
        <p>{{ loadingText }}</p>
      </div>
    </div>
  </div>
  <DiffPopup
    v-if="showDiffPopup"
    :diff="diffResult"
    @confirm="applyDiffToContent"
    @close="showDiffPopup = false"
  />
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { diffChars } from 'diff'
import { useRoute, useRouter } from "vue-router";
import { useThreadStore } from '@/stores/thread'
import DiffPopup from '@/components/threads/spell/DiffPopup.vue'
const threadStore = useThreadStore()

const route = useRoute()
const props = defineProps({
  initialThread: Object, // 없으면 생성 모드
  book: Object
})

const title = ref('')
const content = ref('')
const read_date = ref('')
const loading = ref(false)
const loadingText = ref('')
const diffResult = ref([])
const correctedResult = ref('')
const showDiffPopup = ref(false)

const isCreate = computed(() => {
  return props.initialThread ? false : true
})

// 기존 thread 정보 채우기
watch(() => props.initialThread, (newThread) => {
  if (newThread) {
    title.value = newThread.title
    content.value = newThread.content
    read_date.value = newThread.read_date
  }
}, { immediate: true })


const runSpellCheck = async () => {
  if (!content.value.trim()) return
  loading.value = true
  loadingText.value = '맞춤법 검사 중입니다...'
  try {
    const result  = await threadStore.checkSpelling(content.value)
    correctedResult.value = result.corrected
    diffResult.value = diffChars(content.value, result.corrected)
    showDiffPopup.value = true
  } catch (error) {
    console.error('맞춤법 검사 오류:', error)
  } finally {
    loading.value = false
    loadingText.value = ''
  }
} 

const applyDiffToContent = () => {
  content.value = diffResult.value
    .filter(p => !p.removed)
    .map(p => p.value)
    .join('')
  showDiffPopup.value = false
}


// Thread 생성인지 삭제인지 구분하는 반응형 변수 필요요
const onAddThread = async () => {
  // store.createThread 등 실제 API 연결
  if (!title.value) {
    alert('제목을 입력하세요!')
  } else if (!content.value) {
    alert('내용을 입력하세요!')
  } else if (!read_date.value) {
    alert('날짜를 입력하세요!')
  } else {
    loading.value = true
    loadingText.value = 'Thread 이미지 생성 중입니다...'
    // console.log('제출:', title.value, content.value, read_date.value)
    const payload = {
      title: title.value,
      content: content.value,
      read_date: read_date.value
    }
    try {
      const id = isCreate.value ? route.params.bookId : route.params.threadId
      await threadStore.createThread(isCreate.value, id, payload)
    } catch (err) {
      console.error(err)
    } finally {
      loading.value = false
      loadingText.value = ''
    }
  }
}

</script>

<style scoped>
.thread-form-container {
  flex: 2;
  background-color: #fffefc;
  padding: 2rem 1.5rem; /* ✅ 좌우에 padding 추가 */
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  max-width: 100%;
}

.thread-form {
  width: 100%;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  font-weight: bold;
  color: #5a3b2e;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  display: block;
}

.form-input,
.form-textarea {
   font-family: 'SF_HambakSnow', sans-serif !important;  /*  폰트 적용 */
  width: 100%;
  max-width: 100%;
  box-sizing: border-box; /*  padding 포함한 너비 계산 */
  padding: 0.8rem 1rem;
  font-size: 1rem;
  font-family: 'Gowun Batang', serif;
  border: 1px solid #d0bba6;
  border-radius: 8px;
  background-color: #fffefc;
}

.form-textarea {
  resize: vertical;
  min-height: 180px;
  line-height: 1.6;
}

.submit-btn,
.spellcheck-btn {
  background-color: #b37442;
  color: white;
  border: none;
  padding: 0.6rem 1.4rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.95rem;
  transition: background-color 0.2s;
  display: inline-block;
}

.submit-btn {
  margin-right: 1rem; /*  오른쪽 여백 */
  margin-top: 1.2rem;
}

.spellcheck-btn {
  margin-top: 1.2rem;
}

</style>
<style>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.loading-box {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 50%;
  max-width: 400px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
  text-align: center;
}

.loading-box img {
  width: 120px;
  height: auto;
}
</style>



