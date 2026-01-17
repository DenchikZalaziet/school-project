import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './utils/router'
import { useAuthStore } from './utils/auth_store'

const app = createApp(App)
app.use(createPinia())

useAuthStore().setup();

useAuthStore().$subscribe((mutation, state) => {
  localStorage.setItem('token', state.token)
  localStorage.setItem('user', JSON.stringify(state.user))
})

app.use(router)
app.mount('#app')
