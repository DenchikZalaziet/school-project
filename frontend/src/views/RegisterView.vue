<template>
  <div class="register-container d-flex justify-content-center align-items-center">
    <div class="register-card p-4 rounded shadow">
      <div class="text-center mb-4">
        <h2 class="register-title">Регистрация</h2>
      </div>
      
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="username" class="form-label">Имя</label>
          <input 
            type="text" 
            class="form-control input-field"
            id="username"
            v-model="username"
            required
          >
        </div>
        
        <div class="mb-4">
          <label for="password" class="form-label">Пароль</label>
          <input 
            type="password" 
            class="form-control input-field"
            id="password"
            v-model="password"
            required
          >
        </div>
        
        <button 
          type="submit" 
          class="btn register-btn w-100"
          :disabled="!isFormValid">
          Создать
        </button>
      </form>

      <p v-if="authStore.error_message" class="error-box">{{ authStore.error_message }}</p>
      
      <div class="mt-3 text-center">
        <button type="button" class="btn btn-outline-primary mx-2" @click="redirectToHome">Главная</button>
        <button type="button" class="btn btn-outline-primary mx-2" style="width: 50%" @click="redirectToLogin">Войти</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/utils/auth_store';

const authStore = useAuthStore();
</script>

<script>
export default {
  name: 'Register View',
  data() {
    return {
      username: '',
      password: '',

      loading: false
    }
  },
  computed: {
    isFormValid() {
      return this.username.trim()
      && this.password.trim();
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true;
      useAuthStore().register(this.username.trim(), this.password);
      this.loading = false;
    },
    async redirectToLogin() {
      this.$router.push('/login/');
    },
    async redirectToHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e0f7ff 0%, #f0fdff 100%);
}

.register-card {
  width: 100%;
  max-width: 400px;
  background-color: white;
  border-top: 4px solid #4da6ff;
}

.register-title {
  color: #2c7db6;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.input-field {
  border: 1px solid #c1e3ff;
  padding: 10px 15px;
  transition: all 0.3s;
}

.input-field:focus {
  border-color: #4da6ff;
  box-shadow: 0 0 0 0.25rem rgba(77, 166, 255, 0.25);
}

.register-btn {
  background-color: #4da6ff;
  color: white;
  padding: 10px;
  font-weight: 600;
  transition: all 0.3s;
  border: none;
}

.register-btn:hover {
  background-color: #2c7db6;
  transform: translateY(-2px);
}

.register-btn:disabled {
  background-color: #a0d1ff;
  transform: none;
}

.signup-link {
  color: #4da6ff;
  text-decoration: none;
  font-weight: 500;
}

.signup-link:hover {
  text-decoration: underline;
  color: #2c7db6;
}
</style>
