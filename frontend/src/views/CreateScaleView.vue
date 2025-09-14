<template>
  <Header></Header>
  <div class="container mb-5">
    <div id="app">
      <div class="container mb-5 p-4">
        <div v-if="error_message" class="alert alert-danger" role="alert">
          {{ error_message }}
        </div>
        
        <div v-if="success_message" class="alert alert-success" role="alert">
          {{ success_message }}
        </div>

        <div class="row justify-content-center">
          <form @submit.prevent="submitScale">
            <div class="col-md-10">
              <h2 class="mb-4">Создание гаммы</h2>
              <div class="mb-4">
                <label for="scaleName" class="form-label fw-bold">Название</label>
                <input type="text"
                  class="form-control form-control-lg custom-input scale-name" 
                  id="scaleName" 
                  v-model="current_name"
                  maxlength="20"
                  placeholder="Введите название гаммы"
                  required
                >
              </div>

              <div class="mb-4">
                <label for="scaleCategory" class="form-label fw-bold">Категория</label>
                <input type="text"
                  class="form-control custom-input" 
                  id="scaleCategory" 
                  v-model="current_category"
                  maxlength="20"
                  placeholder="Введите категорию гаммы"
                  required
                >
              </div>

              <div class="mb-4">
                <label for="scaleDescription" class="form-label fw-bold">Описание</label>
                <textarea class="form-control custom-input scale-description" 
                  id="scaleDescription" 
                  rows="3"
                  v-model="current_description"
                  maxlength="100"
                  placeholder="Опишите особенности этой гаммы"
                ></textarea>
              </div>

              <div class="mb-4">
                <label class="form-label fw-bold">Интервалы</label>
                <div class="intervals-container">
                  <div v-for="(interval, index) in current_intervals" :key="index" class="interval-item p-3 mb-2 rounded">
                    <div class="d-flex align-items-center justify-content-between">
                      <div class="d-flex align-items-center gap-2">
                        <input type="number" 
                          class="form-control interval-input" 
                          v-model.number="current_intervals[index]"
                          min="0" 
                          max="12"
                          required
                          style="width: 80px">
                        <span class="text-nowrap fs-5">{{ intervalName(interval) }}</span>
                      </div>
                      
                      <button type="button" 
                        class="btn btn-outline-danger btn-sm remove-button"
                        @click="removeInterval(index)"
                        :disabled="current_intervals.length <= 1">
                        X
                      </button>
                    </div>
                  </div>
                  
                  <button type="button" 
                    class="btn btn-primary mt-2"
                    @click="addInterval(1)">
                    Добавить интервал
                  </button>

                  <div class="d-flex gap-2 justify-content-end mt-4">
                    <button type="submit" class="btn btn-success form-btn mx-4 px-4" :disabled="!isFormValid">
                      <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                      {{ loading ? 'Создание...' : 'Создать гамму' }}
                    </button>
                    <button type="button" class="btn btn-outline-secondary form-btn" @click="resetForm">
                      Сбросить
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue';
import api from '@/utils/axios';
import { useAuthStore } from '@/utils/auth_store';
</script>

<script>
export default {
  name: 'Create Scale View',
  data() {
    return {
      error_message: '',
      success_message: '',
      loading: false,

      current_name: '',
      current_description: '',
      current_category: '',
      current_intervals: [1]
    }
  },
  computed: {
    isFormValid() {
      return !this.loading &&
      this.current_name.trim() && 
      this.current_category.trim() &&
      this.current_intervals != [];
    }
  },
  methods: {
    intervalName(interval) {
      const lastDigit = interval % 10;
      const lastTwoDigits = interval % 100;
      let form;
      if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
          form = 'полутонов';
      } else if (lastDigit === 1) {
          form = 'полутон';
      } else if (lastDigit >= 2 && lastDigit <= 4) {
          form = 'полутона';
      } else {
          form = 'полутонов';
      };
      return form;
    },
    addInterval(value) {
      this.current_intervals.push(value);
    },
    removeInterval(index) {
      if (this.current_intervals.length > 1) {
        this.current_intervals.splice(index, 1);
      }
    },
    resetForm() {
      this.current_name = '';
      this.current_description = '';
      this.current_category = '';
      this.current_intervals = [1];
      this.error_message = '';
      this.success_message = '';
    },
    async submitScale() {
      const data = {
        name: this.current_name.trim(),
        description: this.current_description.trim(),
        category: this.current_category.trim(),
        intervals: this.current_intervals
      };
      
      this.loading = true;
      
      await api.post('scale', data, {
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${useAuthStore().token}`
        }
      })
      .then(response => {
        this.success_message = 'Гамма успешно создана!';
        this.resetForm();
      })
      .catch (error => {
        console.error(error);
        this.error_message = error.response?.data?.detail || "Произошла ошибка";
      })
      .finally (() => {
        this.loading = false;
      });
    }
  }
}
</script>

<style scoped>
.remove-button {
  background-color: white;
}

.remove-button:hover {
  color: rgb(200, 0, 0);
  border-color: rgb(200, 0, 0);
}

.remove-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.scale-name {
  color: var(--dark-blue);
  margin: 0;
  font-size: 1.5rem;
}

.form-label {
  font-size: 1.5;
  margin: 10px;
}

.scale-description {
  color: #444;
  line-height: 1.3rem;
}

.badge {
  background-color: var(--primary-blue);
  font-size: 0.9rem;
  padding: 0.5em 0.75em;
}

.custom-input {
  border: 1px solid var(--border-blue);
  background-color: var(--light-blue);
  color: var(--dark-blue);
}

.interval-item {
  border-left: 3px solid var(--primary-blue);
  background-color: var(--light-blue);
}

.empty-state {
  color: var(--dark-blue);
  background-color: var(--light-blue);
  border-radius: 10px;
  margin-top: 2rem;
  border-top: 4px solid #4da6ff;
}

.interval-input {
  border: 1px solid var(--border-blue);
  background-color: white;
  color: var(--dark-blue);
}

.form-btn {
  min-width: 140px;
}
</style>