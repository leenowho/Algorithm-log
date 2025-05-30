<template>
  <div class="edit-container">
    <h2>프로필 수정</h2>
    <form @submit.prevent="onUpdate">
      <div class="form-item">
        <label for="last-name">아이디</label>
        <input type="text" id="last-name" v-model="form.username">
      </div>
      <div class="form-item">
        <label for="last-name">성</label>
        <input type="text" id="last-name" v-model="form.lastName">
      </div>
      <div class="form-item">
        <label for="first-name">이름</label>
        <input type="text" id="first-name" v-model="form.firstName">
      </div>
      <div class="form-item">
        <!-- 🔸 나이 -->
        <label for="age">나이</label>
        <input id="age" type="number" v-model="form.age" min="0" />
      </div>

      <CategorySelectCard
        v-model="form.interested_categories"
        :categories="categoryList"
      />

      <button type="submit">수정하기</button>
    </form>
    <RouterLink :to="{ name: 'user-password-change'}" class="password-change-link">
      비밀번호 변경하기
    </RouterLink>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useBookStore } from '@/stores/book'
import { useRouter } from 'vue-router'
import CategorySelectCard from '@/components/auth/CategorySelectCard.vue'

const userStore = useUserStore()
const bookStore = useBookStore()
const router = useRouter()
const categoryList = ref(bookStore.categories)

const form = reactive({
  username: userStore.userInfo.username,
  firstName: '',
  lastName: '',
  age: null,
  interested_categories: []
})

onMounted(async () => {
  await userStore.getUserInfo()
  form.username = userStore.userInfo.username
  form.age = userStore.userInfo.age
  form.firstName = userStore.userInfo.first_name
  form.lastName = userStore.userInfo.last_name
  form.interested_categories = userStore.userInfo.interested_categories || []
})

const onUpdate = async () => {
  try {
    const payload = {
      age: form.age,
      first_name: form.firstName,
      last_name: form.lastName,
      interested_categories: form.interested_categories
    }
    if (form.username !== userStore.userInfo.username) {
      payload.username = form.username
    }

    await userStore.updateUserInfo(payload)

    alert('프로필이 수정되었습니다.')
    router.push({ name: 'user-profile'}) // ✅ 메인 페이지로 이동

  } catch (err) {
    console.error('❌ 수정 실패:', err.response?.data)

    // ✅ 중복된 아이디인 경우 따로 처리
    if (err.response?.data?.username?.[0]?.includes('already exists')) {
      alert('이미 존재하는 아이디입니다. 다른 아이디로 수정해주세요.')
    } else {
      alert('수정 실패: ' + (err.response?.data?.detail || '입력값을 확인해주세요.'))
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&display=swap');

.edit-container {
  background-color: #fffaf5;
  max-width: 400px;
  margin: 4rem auto;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  font-family: 'Gowun Batang', serif;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  text-align: center;
  padding: 1rem 2rem;
}
.form-item {
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-bottom: 1rem;
}
.password-change-link {
  display: inline-block;
  margin-top: 1rem;
  color: #6e4b3a;
  font-size: 0.95rem;
  text-decoration: underline;
  transition: color 0.2s;
}

h2 {
  font-size: 1.6rem;
  text-align: center;
  color: #3e2d1d;
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
  color: #5b3926;
}

input {
  padding: 0.6rem 1rem;
  border: 1px solid #d6c1ad;
  border-radius: 8px;
  background-color: #fffdf8;
}

button {
  margin-top: 1rem;
  padding: 0.8rem;
  background-color: #b37442;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 80%;
}
button:hover {
  background-color: #9e6234;
}
</style>
