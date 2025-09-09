<template>
  <Header></Header>
  <div class="profile-card card border-0 shadow-sm d-flex justify-content-center my-4">
    <div class="card-body p-4">
      <form @submit.prevent="submitUserInfo">
      <div class="mb-4">
        <label for="usernameInput" class="ms-2 col-form-label-lg">
        <i class="bi bi-person me-2"></i>Имя
        </label>
        <input 
        type="text" 
        class="form-control input-field border-2 border-primary rounded-3 py-3 px-4" 
        id="usernameInput" 
        v-model="current_username"
        maxlength="20"
        @change="user_info_changed = true"
        placeholder="Имя"
        required
        style="
            border-color: var(--border-blue) !important;
            transition: all 0.3s ease;
        "
        >
      </div>

      <div class="mb-4">
        <label for="usernameInput" class="ms-2 col-form-label-lg">
        <i class="bi bi-person me-2"></i>Описание
        </label>
        <textarea 
        type="text" 
        class="form-control input-field border-2 border-primary rounded-3 py-3 px-4" 
        id="descriptionInput" 
        v-model="current_description"
        maxlength="100"
        @change="user_info_changed = true"
        placeholder="Описание"
        style="
            border-color: var(--border-blue) !important;
            transition: all 0.3s ease;
        ">
        </textarea>
      </div>
      <div class="text-center">
        <p v-if="error_message" class="error-box">{{ error_message }}</p>
        <button type="submit" 
        class="submit-btn btn btn-outline-primary mx-2" 
        :disabled="!isFormValid">
        Изменить
        </button>
      </div>
      </form>
    </div>
  </div>

  <MyScales> </MyScales>
</template>

<script setup>
import Header from '@/components/Header.vue'
import MyScales from '@/components/MyScales.vue';
import { useAuthStore } from '@/utils/auth_store';

const authStore = useAuthStore()
</script>

<script>
import api from '@/utils/axios';

export default {
  name: 'My Profile View',
  data() {
    return {
        error_message: '',

        current_username: useAuthStore().username,
        current_description: useAuthStore().description,
        user_info_changed: false
    }
  },
  methods: { 
    async submitUserInfo() {
      const formData = new FormData()
      formData.append("username", this.current_username)
      formData.append("description", this.current_description)

      await api.patch('/user/me', 
        formData, {
        headers: { 
            "Content-Type": "multipart/form-data"
        }
      })
      .then (response => {
        useAuthStore().fetchUser()
        this.error_message = ''
        this.user_info_changed = false
      })
      .catch (error => {
        this.error_message = error.response?.data?.detail | "Произошла ошибка"
        console.log(error)
      })
    }
  },
  watch: {
  },
  computed: {
    isFormValid() {
      return this.user_info_changed && this.current_username.length > 0
    }
  }
}
</script>

<style scoped> 
.submit-btn {
  background-color: #ffffff;
  padding: 10px;
  font-weight: 600;
  transition: all 0.3s;
  border: 1px solid var(--primary-blue);
  width: 20%;
}

.submit-btn:hover {
  background-color: #2c7db6;
  transform: translateY(-2px);
}

.submit-btn:disabled {
  background-color: #e4f3ff;
  transform: none;
}

.profile-card {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 12px;
  border: 1px solid var(--border-blue);
  background-color: var(--light-blue);
}
</style>