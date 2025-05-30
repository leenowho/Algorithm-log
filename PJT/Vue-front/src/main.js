import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniPluginPersistedstate from 'pinia-plugin-persistedstate'


// ✅ v-calendar 설정
import VCalendar from 'v-calendar'
import 'v-calendar/dist/style.css'

import App from './App.vue'
import router from './router'


const app = createApp(App)
const pinia = createPinia()
pinia.use(piniPluginPersistedstate)

app.use(pinia)
app.use(router)
app.use(VCalendar, {
  componentPrefix: 'v', // <v-calendar>, <v-date-picker> 등 사용 가능
})

app.mount('#app')
