<template>
  <header class="app-header sticky-top bg-white border-bottom">
    <div class="container py-2">
      <div class="d-flex align-items-center">
        
        <router-link to="/" class="d-flex align-items-center text-decoration-none min-width-0 flex-grow-1">
          <img src="../assets/logo.png" class="logo-img flex-shrink-0" alt="Logo">
          <span class="brand-name ms-2 fs-4 fw-bold text-truncate">PolyFret</span>
        </router-link>

        <ul class="nav d-none d-lg-flex px-3">
          <li><router-link to="/" class="nav-link custom-nav-link" active-class="active">Главная</router-link></li>
          <li><router-link :to="{path: '/scales/', query: {page: 1}}" class="nav-link custom-nav-link" active-class="active">Гаммы</router-link></li>
        </ul>

        <div class="auth-actions d-flex align-items-center gap-2 flex-shrink-0">
          <template v-if="authStore.isAuthenticated">
            <router-link :to="{path: '/profile/me/', query: {page: 1}}" class="btn btn-profile btn-outline-primary rounded-pill">
              <i class="bi bi-person-circle"></i>
              <span class="ms-2 d-none d-md-inline">{{ authStore.username }}</span>
            </router-link>
            <button @click="logout" class="btn btn-outline-danger rounded-pill">
              <i class="bi bi-box-arrow-right d-md-none"></i>
              <span class="d-none d-md-inline">Выйти</span>
            </button>
          </template>

          <template v-else>
            <button @click="$router.push('/login')" class="btn btn-outline-primary rounded-pill">
              <i class="bi bi-box-arrow-in-right"></i> <span class="ms-2 d-none d-sm-inline">Вход</span>
            </button>
            <button @click="$router.push('/register')" class="btn btn-primary rounded-pill shadow-sm">
              <i class="bi bi-person-plus-fill"></i> <span class="ms-2 d-none d-sm-inline">Регистрация</span>
            </button>
          </template>
        </div>

      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/utils/auth_store';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout();
  router.push('/');
};
</script>

<style scoped>
.app-header {
  border-top: 4px solid var(--primary-blue);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.logo-img {
  width: 45px;
  height: 45px;
}

.brand-name {
  color: var(--primary-blue);
  white-space: nowrap;
}

.min-width-0 {
  min-width: 0;
}

.auth-actions {
  flex-shrink: 0;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.2s;
  border-width: 1px;
}

.btn-primary {
  background-color: var(--primary-blue);
  border-color: var(--primary-blue);
  box-shadow: 0 4px 12px rgba(var(--primary-blue-rgb, 79, 70, 229), 0.25);
}

.btn-primary:hover {
  background-color: var(--dark-blue);
  border-color: var(--dark-blue);
  box-shadow: 0 8px 18px rgba(var(--primary-blue-rgb, 79, 70, 229), 0.3);
}

.btn-outline-primary {
  color: var(--primary-blue);
  border-color: var(--primary-blue);
}

.btn-outline-primary:hover {
  background-color: var(--primary-blue);
  color: white;
  border-color: var(--primary-blue);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.custom-nav-link {
  color: var(--primary-blue);
  font-weight: 600;
  text-decoration: none;
  position: relative;
  padding: 8px 0;
  transition: color 0.3s ease;
}

.custom-nav-link {
  color: var(--primary-blue);
  font-weight: 600;
  text-decoration: none;
  padding: 8px 16px;
  transition: all 0.3s ease;
  position: relative;
}

.custom-nav-link:hover {
  border-radius: 4px;
  color: var(--dark-blue);
}

.custom-nav-link.active {
  color: var(--dark-blue);
}

.custom-nav-link.active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 16px;
  right: 16px; 
  height: 3px;
  background-color: var(--dark-blue);
  border-radius: 2px;
}

@media (max-width: 576px) {
  .logo-img { width: 40px; height: 40px; }
  .brand-name { font-size: 1.1rem; }
  .btn { padding: 0.4rem 0.75rem; font-size: 0.85rem; }
}

@media (max-width: 380px) {
  .brand-name { display: none; }
}
</style>