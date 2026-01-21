<template>
  <Header></Header>
  <div class="container text-center py-5">
    <div class="hero-section mb-5">
      <h1 class="display-4 fw-bold mb-3 text-gradient">Добро пожаловать!</h1>
      <p class="lead mb-4 fs-4 text-muted">Веб-приложение для создания гамм и визуализации на грифе инструментов</p>
    </div>
    
    <div class="row mt-5 g-4">
      <div class="col-md-4">
        <div class="card feature-card h-100">
          <div class="card-body d-flex flex-column p-4">
            <div class="feature-icon mb-3 fs-1">🎵</div>
            <h5 class="card-title fw-semibold">Создавайте гаммы</h5>
            <p class="card-text flex-grow-1">Создавайте собственные музыкальные гаммы с интервалами</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card feature-card h-100">
          <div class="card-body d-flex flex-column p-4">
            <div class="feature-icon mb-3 fs-1">🎸</div>
            <h5 class="card-title fw-semibold">Визуализируйте на грифе</h5>
            <p class="card-text flex-grow-1">Смотрите гаммы на виртуальном грифе различных инструментов</p>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card feature-card h-100">
          <div class="card-body d-flex flex-column p-4">
            <div class="feature-icon mb-3 fs-1">📚</div>
            <h5 class="card-title fw-semibold">Изучайте публичные гаммы</h5>
            <p class="card-text flex-grow-1">Просматривайте гаммы, созданные другими пользователями</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="cta-section mt-5 pt-4">
      <router-link :to="{path: '/scales/', query: {page: 1}}" class="btn btn-primary btn-lg mx-2 mb-2">
        Смотреть гаммы
      </router-link>
      <router-link to="/scales/create/" class="btn btn-outline-primary btn-lg mx-2 mb-2" v-if="isAuthenticated">
        Создать гамму
      </router-link>
      <router-link to="/login/" class="btn btn-outline-primary btn-lg mx-2 mb-2" v-else>
        Войти
      </router-link>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue';
import { useAuthStore } from '@/utils/auth_store';
import { computed } from 'vue';

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);
</script>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.hero-section {
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.text-gradient {
  background: linear-gradient(90deg, var(--primary-blue), var(--dark-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.feature-card {
  border: 2px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
  border-color: rgba(var(--primary-blue-rgb, 79, 70, 229), 0.2);
}

.feature-icon {
  opacity: 0.9;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

/* Улучшенные стили для кнопок */
.btn-primary, .btn-outline-primary {
  padding: 0.75rem 2rem;
  border-radius: 8px;
  font-weight: 500;
  letter-spacing: 0.3px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background-color: var(--primary-blue);
  border-color: var(--primary-blue);
  box-shadow: 0 4px 12px rgba(var(--primary-blue-rgb, 79, 70, 229), 0.25);
}

.btn-primary:hover {
  background-color: var(--dark-blue);
  border-color: var(--dark-blue);
  transform: translateY(-3px);
  box-shadow: 0 8px 18px rgba(var(--primary-blue-rgb, 79, 70, 229), 0.3);
}

.btn-outline-primary {
  color: var(--primary-blue);
  border-color: var(--primary-blue);
  border-width: 2px;
}

.btn-outline-primary:hover {
  background-color: var(--primary-blue);
  color: white;
  border-color: var(--primary-blue);
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.cta-section {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  padding-top: 2rem;
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2.5rem;
  }
  
  .hero-section p {
    font-size: 1.1rem;
  }
  
  .btn-lg {
    padding: 0.6rem 1.5rem;
    font-size: 1rem;
    display: block;
    width: 100%;
    margin-bottom: 0.75rem;
  }
  
  .mx-2 {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
}
</style>
