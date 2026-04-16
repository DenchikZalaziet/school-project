<template>
  <MusicBackground />
  <Header />
  <div class="container mb-5 p-4">
    <div class="row justify-content-center">
      <form @submit.prevent="submitScale" class="col-md-10">
        <h2 class="mb-4">Создание гаммы</h2>
        
        <div v-if="error_message" class="alert alert-danger mb-4">{{ error_message }}</div>

        <div class="mb-4">
          <label for="scaleName" class="form-label fw-bold text-secondary text-uppercase small tracking-wider">Название</label>
          <input type="text" class="form-control form-control-lg custom-input" 
            id="scaleName" v-model="current_name" maxlength="50" 
            placeholder="Введите название" required>
        </div>

        <div class="mb-4">
          <label for="scaleCategory" class="form-label fw-bold text-secondary text-uppercase small tracking-wider">Категория</label>
          <input type="text" class="form-control custom-input" 
            id="scaleCategory" v-model="current_category" maxlength="30" 
            placeholder="Введите категорию" required>
        </div>

        <div class="mb-4">
          <label for="scaleDescription" class="form-label fw-bold text-secondary text-uppercase small tracking-wider">Описание</label>
          <textarea class="form-control custom-input" 
            id="scaleDescription" rows="3" v-model="current_description" 
            maxlength="70" placeholder="Опишите особенности этой гаммы"></textarea>
        </div>

        <div class="mb-4">
          <label class="form-label fw-bold text-secondary text-uppercase small tracking-wider">Интервалы</label>
          <div class="intervals-container">
            <div v-for="(interval, index) in current_intervals" :key="index" class="interval-item p-3 mb-2 rounded shadow-sm">
              <div class="d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center gap-2">
                  <input type="number" class="form-control interval-input" v-model.number="current_intervals[index]"
                    min="0" max="12" style="width: 80px">
                  <span class="text-nowrap fs-5">{{ intervalName(interval) }}</span>
                </div>
                
                <button type="button" class="btn btn-outline-danger btn-sm border-0"
                  @click="removeInterval(index)" :disabled="current_intervals.length <= 1">✕</button>
              </div>
            </div>
              
            <div class="d-flex align-items-center gap-3 mt-3">
              <button type="button" class="btn btn-primary px-5 rounded-pill" @click="addInterval(1)">+ Добавить</button>
              <ScalePlayer :intervals="current_intervals" />
            </div>

            <div class="d-flex flex-wrap gap-2 justify-content-end mt-5 border-top pt-4">
              <button type="button" class="btn btn-outline-secondary rounded-pill px-4" @click="resetForm">Сбросить</button>
              <div @click="handleDisabledSaveClick" class="d-inline-block">
                <button type="submit" class="btn btn-success form-btn rounded-pill px-4" :disabled="!isFormValid">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                  {{ loading ? '...' : 'Создать гамму' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>

    <div class="modal fade" id="createSuccessModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-success text-white border-0"><h5 class="modal-title">Успешно!</h5></div>
          <div class="modal-body py-4 text-center fs-5">Гамма <strong>{{ created_name }}</strong> успешно создана.</div>
          <div class="modal-footer border-0">
            <button class="btn btn-success rounded-pill px-4" data-bs-dismiss="modal" @click="goToScales">К списку гамм</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="createHintModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-warning text-dark border-0"><h5 class="modal-title">Внимание</h5></div>
          <div class="modal-body py-4">Пожалуйста, заполните название и категорию гаммы.</div>
          <div class="modal-footer border-0"><button class="btn btn-dark rounded-pill px-4" data-bs-dismiss="modal">Понятно</button></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import MusicBackground from '@/components/MusicBackground.vue';
import ScalePlayer from '@/components/ScalePlayer.vue';
import { useAuthStore } from '@/utils/auth_store';
import { api } from '@/utils/axios';
import { Modal } from 'bootstrap';

export default {
  name: 'CreateScaleView',
  components: {
    Header,
    MusicBackground,
    ScalePlayer
  },
  data() {
    return {
      loading: false, 
      error_message: '', 
      current_name: 'Новая гамма', 
      current_description: '', 
      current_category: 'Приватная', 
      current_intervals: [2, 2, 1, 2, 2, 2, 1],
      created_name: ''
    }
  },
  computed: {
    isFormValid() {
      return !this.loading && 
             this.current_name.trim() !== '' && 
             this.current_category.trim() !== '' && 
             this.current_intervals.length > 0;
    }
  },
  methods: {
    handleDisabledSaveClick() {
      if (!this.isFormValid && !this.loading) {
        new Modal(document.getElementById('createHintModal')).show();
      }
    },

    intervalName(interval) {
      const v = Math.abs(interval);
      const lastDigit = v % 10; const lastTwoDigits = v % 100;
      if (lastTwoDigits >= 11 && lastTwoDigits <= 14) return 'полутонов';
      if (lastDigit === 1) return 'полутон';
      if (lastDigit >= 2 && lastDigit <= 4) return 'полутона';
      return 'полутонов';
    },

    addInterval(v) { this.current_intervals.push(v); },
  
    removeInterval(i) { this.current_intervals.splice(i, 1); },
  
    resetForm() {
      this.current_name = ''; 
      this.current_description = ''; 
      this.current_category = ''; 
      this.current_intervals = [2, 2, 1, 2, 2, 2, 1];
    },

    goToScales() {
      this.$router.push('/scales');
    },

    async submitScale() {
      this.loading = true;
      await api.post('/scale', {
        name: this.current_name.trim(), 
        description: this.current_description.trim(),
        category: this.current_category.trim(), 
        intervals: this.current_intervals
      }, { 
        headers: { 'Authorization': `Bearer ${useAuthStore().token}` }
      })
      .then(response => {
        this.created_name = this.current_name;
        this.resetForm();
        new Modal(document.getElementById('createSuccessModal')).show();
      })
      .catch(error => {
        this.error_message = "Ошибка при создании гаммы";
      })
      .finally(() => {
        this.loading = false;
      });
    }
  }
}
</script>

<style scoped>
.custom-input { 
  border: 1px solid var(--border-blue); 
  background-color: var(--light-blue); 
  transition: border-color 0.2s, box-shadow 0.2s;
}

.custom-input:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.15);
  background-color: #fff;
}

.interval-item { 
  border-left: 4px solid #007bff; 
  background-color: #f8f9fa; 
}

.interval-input {
  text-align: center;
  border: 1px solid var(--border-blue);
}

.form-btn { 
  min-width: 160px; 
}
</style>