<template>
  <header class="p-2 border-bottom app-header">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <router-link :to="`/profile/me`" class="logo-container d-flex lign-items-center">
          <img src="../assets/logo.png" class="logo"  alt="Лого" width="70" height="70">
        </router-link>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <router-link :to="`/`" class="header-link"><a class="nav-link px-2 text-secondary">Главная</a></router-link>
          <router-link :to="`/scales`" class="header-link"><a class="nav-link px-2 text-secondary">Гаммы</a></router-link>
        </ul>

        <div class="text-end" v-if="authStore.isAuthenticated">
          <router-link :to="`/profile/me`" class="header-link">
            <a href="#" class="btn btn-outline-primary rounded-pill px-4 mx-2 shadow-sm">
              <i class="bi bi-person me-2"></i> {{ authStore.username }}
            </a>
          </router-link>
          <button type="button" class="btn btn-primary mx-2" @click="logout">Выйти</button>
        </div>

        <div class="text-end" v-else>
          <button type="button" class="btn btn-outline-primary me-2 px-4" @click="$router.push('/login')">Вход</button>
          <button type="button" class="btn btn-primary" @click="$router.push('/register')">Регистрация</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/utils/auth_store';

const authStore = useAuthStore();
</script>

<script>
export default {
  name: 'Header',
  methods: {
    async logout() {
      useAuthStore().logout();
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.header-link { 
  text-decoration: none; 
}
  
.app-header {
  background-color: white;
  border-top: 4px solid var(--primary-blue);
  border-bottom: 1px solid var(--border-blue);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
  
.logo {
  color: var(--primary-blue);
  font-size: 1.5rem;
  gap: 10px;
  transition: all 0.1s;
}

.logo:hover, .logo.active {
  transform: scale(1.1);
  transition: all 0.3s;
}

.nav-link {
  color: #333;
  font-weight: 500;
  position: relative;
  padding: 0.5rem 1rem !important;
  transition: all 0.3s;
}

.nav-link:hover, .nav-link.active {
  transform: translateY(-2px);
  color: var(--primary-blue);
}

.nav-link:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: var(--primary-blue);
  transition: all 0.3s;
  transform: translateX(-50%);
}

.nav-link:hover:after, .nav-link.active:after {
  width: 70%;
}

.btn-outline-primary {
  color: var(--primary-blue);
  border-color: var(--primary-blue);
}

.btn-outline-primary:hover {
  background-color: var(--primary-blue);
  color: white;
}

.btn-primary {
  background-color: var(--primary-blue);
  border-color: var(--primary-blue);
  transition: all 0.3s;
}

.btn-primary:hover {
  background-color: var(--dark-blue);
  border-color: var(--dark-blue);
  transform: translateY(-2px);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #333;
  font-weight: 500;
}
</style>
