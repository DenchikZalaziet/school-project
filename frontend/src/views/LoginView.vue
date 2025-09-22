<template>
  <div class="login-container d-flex justify-content-center align-items-center">
    <div class="login-card p-4 rounded shadow">
      <div class="text-center mb-4">
        <h2 class="login-title">Вход</h2>
      </div>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="username" class="form-label">Имя</label>
          <input 
            type="text" 
            class="form-control input-field"
            id="username"
            maxlength="20"
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
          class="btn login-btn w-100"
          :disabled="!isFormValid">
          Войти
        </button>
      </form>

      <p v-if="error_message" class="error-box">{{ error_message }}</p>
      
      <div class="mt-3 text-center">
        <button type="button" class="btn btn-outline-primary mx-2" @click="redirectToHome">Главная</button>
        <button type="button" class="btn btn-outline-primary mx-2" style="width: 50%" @click="redirectToRegister">Создать аккаунт</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/utils/auth_store';
</script>

<script>
export default {
  name: 'Login View',
  data() {
    return {
      username: '',
      password: '',

      error_message: ''
    }
  },
  computed: {
    isFormValid() {
      return this.username.trim()
      && this.password.trim();
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      await useAuthStore().login(this.username.trim(), this.password);
      this.error_message = useAuthStore().error_message;
      this.loading = false;
    },
    async redirectToRegister() {
      this.$router.push('/register');
    },
    async redirectToHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #e0f7ff 0%, #f0fdff 100%);
}

.login-card {
  width: 100%;
  max-width: 400px;
  background-color: white;
  border-top: 4px solid #4da6ff;
}

.login-title {
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

.login-btn {
  background-color: #4da6ff;
  color: white;
  padding: 10px;
  font-weight: 600;
  transition: all 0.3s;
  border: none;
}

.login-btn:hover {
  background-color: #2c7db6;
  transform: translateY(-2px);
}

.login-btn:disabled {
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