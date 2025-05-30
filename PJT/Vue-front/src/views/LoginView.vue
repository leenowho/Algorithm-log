<template>
  <div class="login-container">
    <div class="login-box">
      <h2>📚 로그인</h2>
      <form @submit.prevent="onLogin">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model="username" />

        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model="password" />

        <button type="submit">로그인</button>
      </form>

      <!-- ✅ 회원가입 유도 링크 추가 -->
      <RouterLink :to="{ name: 'user-signup'}" class="signup-link">
        계정이 없으신가요? 회원가입
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const userStore = useUserStore()
const router = useRouter()

const onLogin = async () => {
  await userStore.login({
    username: username.value,
    password: password.value
  })
  if (userStore.accessToken) {
    alert('로그인 성공!')
    router.push({ name: 'Main' })
  }
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&display=swap');

.login-container {
  background-color: #f3e5d8;
  /* min-height: 100vh; */
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Gowun Batang', serif;
  padding: 2rem;
}

.login-box {
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
  max-width: 400px;
}

label {
  font-size: 1rem;
  color: #5b3926;
  text-align: left;
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

/* ✅ 회원가입 링크 스타일 */
.signup-link {
  display: inline-block;
  margin-top: 1rem;
  color: #6e4b3a;
  font-size: 0.95rem;
  text-decoration: underline;
  transition: color 0.2s;
}
.signup-link:hover {
  color: #9e6234;
}
</style>
