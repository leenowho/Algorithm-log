<template>
  <section class="logout-info">
    <div class="message-box">
      <h2>👋 당신의 이야기는 잠시 쉬어갑니다.</h2>
      <p>마음이 머무는 곳에서, 다시 이어가실 준비가 되면<br />우린 여기서 기다릴게요.</p>
      <p class="choice">어디로 가시겠습니까?</p>
    </div>
    <div class="button-group">
      <RouterLink :to="{ name: 'Main' }" class="action-button">📚 메인으로 돌아가기</RouterLink>
      <RouterLink :to="{ name: 'user-login' }" class="action-button">🔑 다시 로그인</RouterLink>
    </div>
  </section>
</template>

<style scoped>
.logout-info {
  text-align: center;
  margin-top: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.message-box {
  background-color: #fff3e4; /* 기존 배경과 대비되는 따뜻한 배경색 */
  border-radius: 12px;
  padding: 2rem 2.5rem;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  margin-bottom: 2rem;
}

.message-box h2 {
  margin-bottom: 1rem;
  font-weight: bold;
  font-size: 1.5rem;
  color: #3c2e1a;
}

.message-box p {
  margin: 0.5rem 0;
  color: #5e4b36;
  font-size: 1rem;
}

.message-box .choice {
  margin-top: 1.2rem;
  font-weight: 500;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.action-button {
  background-color: #f4c28d;
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  color: white;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #e1a76c;
}
</style>
