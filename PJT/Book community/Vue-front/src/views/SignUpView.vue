<template>
  <div class="signup-container">
    <div class="signup-box">
      <h2>📚 회원가입</h2>
      <form @submit.prevent="onSignup" class="form-group">
        <div class="form-item">
          <label for="username">아이디 (5~15자 영문/숫자)</label>
          <input type="text" id="username" v-model="form.username" />
        </div>

        <div class="form-item">
          <label for="password1">비밀번호 (8자 이상,영문/숫자/특수문자 포함)</label>
          <input type="password" id="password1" v-model="form.password1" />
        </div>

        <div class="form-item">
          <label for="password2">비밀번호 확인</label>
          <input type="password" id="password2" v-model="form.password2" />
        </div>

        <div class="form-item">
          <label for="age">나이</label>
          <input type="number" id="age" v-model="form.age" min="0" />
        </div>
        <div class="form-item">
          <CategorySelectCard
            v-model="form.interested_categories"
            :categories="categoryList"
          />
        </div>

        <button type="submit">가입하기</button>
      </form>

      <RouterLink :to="{ name: 'user-login'}" class="login-link">이미 계정이 있으신가요? 로그인</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useBookStore } from '@/stores/book'
import CategorySelectCard from '@/components/auth/CategorySelectCard.vue'

const form = ref({
  username: '',
  password1: '',
  password2: '',
  age: '',
  interested_categories: []  // ✅ 선택된 카테고리 id 배열
})
const router = useRouter()
const userStore = useUserStore()
const bookStore = useBookStore()
const categoryList = ref(bookStore.categories)

const onSignup = async () => {
  try {
    await userStore.signup(form.value)
    alert('회원가입 성공! 로그인 페이지로 이동합니다.')
    router.push({ name: 'user-login' })
  } catch (err) {
    alert(err.message || '회원가입에 실패했습니다.')
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&display=swap');

.signup-container {
  background-color: #f3e5d8;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Gowun Batang', serif;
  padding: 2rem;
}

.signup-box {
  text-align: center;
}

h2 {
  font-size: 2rem;
  color: #3e2d1d;
  margin-bottom: 2rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: #fffaf5;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 450px;
}

.form-item {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  font-size: 1rem;
  color: #5b3926;
  margin-bottom: 0.4rem;
}

input {
  padding: 0.6rem 1rem;
  border: 1px solid #d6c1ad;
  border-radius: 8px;
  background-color: #fffdf8;
  font-family: 'Gowun Batang', serif;
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
}
button:hover {
  background-color: #9e6234;
}

/* 로그인으로 돌아가기 */
.login-link {
  display: inline-block;
  margin-top: 1.5rem;
  color: #6e4b3a;
  font-size: 0.95rem;
  text-decoration: underline;
  transition: color 0.2s;
}
.login-link:hover {
  color: #9e6234;
}
</style>
