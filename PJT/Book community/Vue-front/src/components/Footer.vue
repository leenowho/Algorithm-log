<template>
  <footer class="site-footer">
    <div class="footer-content">
      <p>책타래 - 도서 추천 & 커뮤니티 서비스</p>
      <p>🛠 프로젝트 기간: 2025.05.22 ~ 2025.05.27</p>
      <!-- <p>
        🔗 <a href="https://github.com/your-id/your-repo" target="_blank">깃허브 프로젝트 바로가기</a>
      </p> -->
      <p class="copyright">© 2025 책타래 팀. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  background-color: #f3e9dc;
  color: #5a3e2b;
  text-align: center;
  padding: 0.8rem 1rem;
  font-size: 0.85rem;
  line-height: 1.4;
  border-top: 1px solid #d6c6b9;

  /* ✅ 항상 하단 고정 */
  position: relative;
  bottom: 0;
  left: 0;
  /* width: 100%; */
  margin-top: auto;
}

.footer-content {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.footer-content p {
  margin: 0; /* ✅ 여기 추가 */
}

.footer-content a {
  color: #bf5d1f;
  font-weight: bold;
  text-decoration: none;
}

.footer-content a:hover {
  text-decoration: underline;
}
</style>

