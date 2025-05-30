<template>
  <div class="password-change-container">
    <h2>🔐 비밀번호 변경</h2>
    <form @submit.prevent="onChange">
      <label for="old">기존 비밀번호</label>
      <input type="password" id="old" v-model="old" required /><hr>
      <label for="new1">새 비밀번호</label>
      <input type="password" id="new1" v-model="new1" required /><hr>
      <label for="new2">새 비밀번호 확인</label>
      <input type="password" id="new2" v-model="new2" required /><hr>
      <button type="submit">변경하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const old = ref('')
const new1 = ref('')
const new2 = ref('')
const router = useRouter()
const userStore = useUserStore()

const onChange = async () => {
  if (new1.value !== new2.value) {
    alert('❌ 새 비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    await userStore.changePassword({
      old_password: old.value,
      new_password1: new1.value,
      new_password2: new2.value
    })

    alert('✅ 비밀번호가 성공적으로 변경되었습니다.')
    router.push('/main')
  } catch (err) {
    const data = err.response?.data
    if (data?.old_password) {
      alert('❌ 기존 비밀번호가 틀렸습니다.')
    } else if (data?.new_password2) {
      alert('❌ 새 비밀번호 확인이 일치하지 않습니다.')
    } else {
      alert('❌ 비밀번호 변경 실패: 다시 확인해주세요.')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&display=swap');

.password-change-container {
  background-color: #fffaf5;
  max-width: 400px;
  margin: 4rem auto;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  font-family: 'Gowun Batang', serif;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

h2 {
  text-align: center;
  font-size: 1.6rem;
  color: #3e2d1d;
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
  color: #5b3926;
  margin-bottom: 0.3rem;
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
}
button:hover {
  background-color: #9e6234;
}
</style>
