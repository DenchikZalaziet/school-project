<template>
  <MusicBackground />
  <Header />
  <div class="profile-card card border-0 shadow-sm d-flex justify-content-center my-4">
    <div class="card-body p-4">
      <form @submit.prevent="submitUserInfo">
        <h2 class="mb-4 fw-bold">Настройки профиля</h2>

        <div class="mb-4">
          <label for="usernameInput" class="ms-2 form-label fw-bold">
            <i class="bi bi-person me-2"></i>Имя
          </label>
          <input 
            type="text" 
            class="form-control input-field border-2 rounded-3 py-3 px-4" 
            id="usernameInput" 
            v-model="current_username"
            maxlength="20"
            @input="user_info_changed = true"
            placeholder="Имя"
            required
          >
        </div>

        <div class="mb-4">
          <label for="descriptionInput" class="ms-2 form-label fw-bold">
            <i class="bi bi-chat-left-text me-2"></i>Описание
          </label>
          <textarea 
            class="form-control input-field border-2 rounded-3 py-3 px-4" 
            id="descriptionInput" 
            v-model="current_description"
            @input="user_info_changed = true"
            placeholder="Расскажите о себе"
            rows="3">
          </textarea>
        </div>

        <div class="text-center mt-5 border-top pt-4">
          <div v-if="error_message" class="alert alert-danger mb-3">{{ error_message }}</div>
          
          <div class="d-flex justify-content-center gap-3">
            <div @click="handleDisabledSaveClick" class="d-inline-block">
              <button type="submit" 
                class="btn btn-primary rounded-pill px-5 py-2 fw-bold" 
                :disabled="!isFormValid">
                {{ loading ? '...' : 'Сохранить изменения' }}
              </button>
            </div>

            <button type="button" 
              class="btn btn-outline-danger rounded-pill px-4"
              @click="triggerDeleteModal">
              Удалить аккаунт
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>

  <MyScales />

  <div class="modal fade" id="deleteAccountModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-danger text-white border-0">
          <h5 class="modal-title fw-bold">Удаление аккаунта</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body py-4">
          <p class="fs-5 mb-0">Вы уверены? Это действие <strong>необратимо</strong></p>
        </div>
        <div class="modal-footer border-0">
          <button class="btn btn-danger rounded-pill px-4" data-bs-dismiss="modal" @click="confirmDeleteAccount">Да, удалить мой аккаунт</button>
          <button class="btn btn-outline-secondary rounded-pill px-4" data-bs-dismiss="modal">Отмена</button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="profileSuccessModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-success text-white border-0">
          <h5 class="modal-title">Успешно</h5>
        </div>
        <div class="modal-body py-4 text-center fs-5">Профиль обновлен!</div>
        <div class="modal-footer border-0">
          <button class="btn btn-success rounded-pill px-4" data-bs-dismiss="modal">Ок</button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="profileHintModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        <div class="modal-header bg-warning text-dark border-0">
          <h5 class="modal-title">Информация</h5>
        </div>
        <div class="modal-body py-4">{{ hint_message }}</div>
        <div class="modal-footer border-0">
          <button class="btn btn-dark rounded-pill px-4" data-bs-dismiss="modal">Понятно</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue';
import MusicBackground from '@/components/MusicBackground.vue';
import MyScales from '@/components/MyScales.vue';
import { useAuthStore } from '@/utils/auth_store';
import { api } from '@/utils/axios';
import { Modal } from 'bootstrap';
</script>

<script>
export default {
  name: 'MyProfileView',
  components: {
    Header,
    MusicBackground
  },
  data() {
    return {
      error_message: '',
      hint_message: '',
      current_username: useAuthStore().username,
      current_description: useAuthStore().description,
      user_info_changed: false,
      loading: false
    }
  },
  computed: {
    isFormValid() {
      return !this.loading 
        && this.user_info_changed 
        && this.current_username.trim() !== '';
    }
  },
  methods: {
    handleDisabledSaveClick() {
      if (!this.isFormValid && !this.loading) {
        if (!this.user_info_changed) {
          this.hint_message = "Вы не внесли никаких изменений.";
        } else if (this.current_username.trim() === '') {
          this.hint_message = "Имя пользователя не может быть пустым.";
        }
        new Modal(document.getElementById('profileHintModal')).show();
      }
    },

    triggerDeleteModal() {
      new Modal(document.getElementById('deleteAccountModal')).show();
    },

    async confirmDeleteAccount() {
      await api.delete('/user/me', {
        headers: { 'Authorization': `Bearer ${useAuthStore().token}` }
      })
      .then(response => {
        useAuthStore().logout();
        this.$router.push('/');
      })
      .catch(error => {
        this.error_message = "Не удалось удалить аккаунт.";
      });
    },
  
    async submitUserInfo() {
      this.loading = true;
      const formData = new FormData();
      formData.append("username", this.current_username.trim());
      formData.append("description", this.current_description ? this.current_description.trim() : "");

      api.patch('/user/me', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      .then(async response => {
        await useAuthStore().fetchUser();
        this.error_message = '';
        this.user_info_changed = false;
        new Modal(document.getElementById('profileSuccessModal')).show();
      }) 
      .catch(error => {
        this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
      }) 
      .finally(() => {
        this.loading = false;
      });
    }
  }
}
</script>

<style scoped>
.input-field {
  border-color: var(--border-blue);
  transition: all 0.2s ease;
}
.input-field:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
}
.profile-card {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 16px;
  background-color: #f9fcff;
}
</style>