import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from '@/plugins/axios'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import MainView from '@/views/MainView.vue'  
import UserEditView from '@/views/UserEditView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import PasswordChangeView from '@/views/PasswordChangeView.vue'
import ThreadView from '@/views/ThreadView.vue'
import ThreadCreate from '@/components/threads/ThreadCreate.vue'
import ThreadUpdate from '@/components/threads/ThreadUpdate.vue'
import AuthLayoutView from '@/views/AuthLayoutView.vue'
import BookListView from '@/views/BookListView.vue'
import ThreadList from '@/components/threads/ThreadList.vue'
import ThreadDetail from '@/components/threads/ThreadDetail.vue'
import ProfileView from '@/views/ProfileView.vue'
import ChatBot from '@/components/ChatBot.vue'
import FavoriteBookList from '@/components/profiles/FavoriteBookList.vue'
import MyThreadList from '@/components/profiles/MyThreadList.vue'
import BookRecommendList from '@/components/books/BookRecommendList.vue'
import LogoutInfoView from '@/components/auth/LogoutInfoView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/user',
      component: AuthLayoutView,
      children: [
        { path: '',                name: 'user-profile',         component: ProfileView },
        { path: 'login',           name: 'user-login',           component: LoginView },
        { path: 'signup',          name: 'user-signup',          component: SignUpView },
        { path: 'password-change', name: 'user-password-change', component: PasswordChangeView },
        { path: 'edit',            name: 'user-edit',            component: UserEditView },
        { path: 'favorite-books',  name: 'user-favorite-books',  component: FavoriteBookList},
        { path: 'my-threads',      name: 'user-threads',         component: MyThreadList},
        { path: 'logout',          name: 'logout-info',          component: LogoutInfoView},

      ]
    },
    {
      path: '',
      name: 'Main',
      component: MainView // 로그인 성공 시 이동할 메인 페이지
    },
    {
      path: '/books',
      name: 'book-list',
      component: BookListView,
    },
    { 
      path: '/books/:bookId',        
      name: 'book-detail',         
      component: BookDetailView 
    },
    { 
      path: '/books/recommend-list', 
      name: 'book-recommend-list', 
      component: BookRecommendList, },
    {
      path: '/threads',
      name: 'threads',
      component: ThreadView,
      children: [
        { path: '',                 name: 'thread-list',   component: ThreadList },
        { path: ':bookId/create',   name: 'thread-create', component: ThreadCreate },
        { path: ':threadId/update', name: 'thread-update', component: ThreadUpdate, 
          beforeEnter: async (to, from, next) => {
            const userStore = useUserStore()
            const threadId = to.params.threadId

            try {
              const res = await axios.get(`/api/v1/threads/${threadId}/`)
              const threadOwner = res.data.user
              if (userStore.userInfo.username !== threadOwner) {
                alert('작성자만 수정할 수 있습니다.')
                return next({ name: 'thread-list' })
              }
              next()
            } catch (err) {
              alert('존재하지 않는 thread이거나 접근할 수 없습니다.')
              next({ name: 'thread-list' })
            }
          } 
        },
        { path: ':threadId', name: 'thread-detail', component: ThreadDetail },
      ]
    },
    {
      path: '/chatbot',
      name: 'chat-bot',
      component: ChatBot
    },
]
})
// 주의! router 전역 guard 설정하기!!!!
// login되지 않은 사용자가 create / update / delete에 접근하려는 경우 모두 해당

// TODO: 전역 가드에서 인증 체크
router.beforeEach((to, from, next) => {
  const store = useUserStore()
  const publicPages = ['user-signup', 'user-signup']
  const authRequired = !publicPages.includes(to.name)

  const privatePages = [
    'thread-create', 'thread-update', 'user-edit', 'user-password-change',
    'book-recommend-list', 'user-threads', 'user-favorite-books'
  ]
  const notValidPage = privatePages.includes(to.name)
  // 1. 이동하려는 페이지가 post와 관련된 페이지고, 로그인과 관련된 페이지가 아닐 때.
  // 2. 그리고 로그인 되어 있지 않다면

  if (notValidPage && authRequired && !store.isLogin) {
    alert('로그인하지 않은 사용자는 독후감을 작성할 수 없습니다. \n로그인 후 이용해주세요.')
    return next({ name: 'user-login' })
  }
  next()
})
export default router