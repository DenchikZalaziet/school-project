<template>
  <Header></Header>
  <div class="container mb-5 p-4">
    <div v-if="no_content" class="empty-state text-center py-5">
      <h2>{{ no_content_message }}</h2>
    </div>

    <div v-else class="row justify-content-center">
      <form @submit.prevent="submitScale">
        <div class="col-md-10">
          <div class="mb-4">
            <label for="scaleName" class="form-label fw-bold">Название</label>
            <input type="text"
              class="form-control form-control-lg custom-input scale-name" 
              id="scaleName" 
              @change="scale_info_changed = true"
              v-model="current_name"
              maxlength="20"
              placeholder="Имя"
              :disabled="!is_my_scale"
            >
          </div>

          <div class="mb-4">
            <label for="scaleCategory" class="form-label fw-bold">Категория</label>
            <div class="by-1">
              <span class="badge rounded-pill">{{ current_category }}</span>
            </div>
          </div>

          <div class="mb-4">
            <label for="scaleDescription" class="form-label fw-bold">Описание</label>
            <textarea class="form-control custom-input scale-description" 
              id="scaleDescription" 
              rows="3"
              @change="scale_info_changed = true"
              v-model="current_description"
              maxlength="100"
              placeholder="Описание"
              :disabled="!is_my_scale"
            >
            </textarea>
          </div>

          <div class="mb-4">
            <label class="form-label fw-bold">Интервалы</label>
            <div class="intervals-container">
              <div v-for="(interval, index) in current_intervals" :key="index" class="interval-item p-3 mb-2 rounded">
                <div class="d-flex align-items-center justify-content-between">
                  <span v-if="!is_my_scale" class="interval-number fs-5">{{ interval + ' ' + intervalName(interval) }}</span>
                  
                  <div v-else class="d-flex align-items-center gap-2">
                    <input type="number" 
                      class="form-control interval-input" 
                      v-model.number="current_intervals[index]"
                      min="0" 
                      max="12"
                      @change="scale_info_changed = true"
                      style="width: 80px">
                    <span class="text-nowrap fs-5">{{ intervalName(interval) }}</span>
                  </div>
                  
                  <button v-if="is_my_scale" 
                    type="button" 
                    class="btn btn-outline-danger btn-sm remove-button"
                    @click="removeInterval(index); scale_info_changed = true"
                    :disabled="current_intervals.length <= 1">
                    X
                  </button>
                </div>
              </div>
                
              <button v-if="is_my_scale" 
                type="button" 
                class="btn btn-primary mt-2"
                @click="addInterval(1); scale_info_changed = true">
                Добавить интервал
              </button>

              <div v-if="is_my_scale" class="d-flex gap-2 justify-content-end mt-4">
                <button type="submit" class="btn btn-success form-btn mx-1 px-4" :disabled="!isFormValid">
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                {{ loading ? 'Сохранение...' : 'Сохранить' }}
                </button>
                <button type="button" class="btn btn-outline-secondary form-btn mx-1 px-4" @click="resetForm" :disabled="!scale_info_changed">
                  Сбросить
                </button>
                <button type="button" class="btn btn-danger form-btn ms-4" @click="deleteScale">Удалить</button>
              </div>
              <div class="d-flex gap-2 justify-content-end mt-4">
                <button
                  type="button" 
                  class="btn btn-outline-primary" 
                  :data-bs-toggle="scale_info_changed ? 'modal' : null"
                  :data-bs-target="scale_info_changed ? '#saveModal' : null"
                  @click="!scale_info_changed && redirectToInstrument()"
                >
                  Отобразить на инструменте
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>

      <div class="modal fade" id="saveModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Вы хотите сохранить изменения?</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-footer d-flex justify-content-between align-items-center">
              <router-link :to="instrumentRedirectPath" class="router-link">
                <button type="button" class="btn btn-primary m-1" data-bs-dismiss="modal" @click="submitScale">Сохранить</button>
                <button type="button" class="btn btn-outline-secondary m-1" data-bs-dismiss="modal" @click="resetForm">Сбросить</button>
              </router-link>
              <button type="button" class="btn btn-danger m-1" data-bs-dismiss="modal">Отмена</button>
            </div>
          </div>
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
  name: 'Scale By Id View',
  data() {
    return {
      error_message: '',
      no_content: false,
      no_content_message: '',
      loading: false,

      scale_info_changed: false,

      scale_id: this.$route.params.scale_id,
      is_my_scale: false,

      current_name: '',
      current_description: '',
      current_category: '',
      current_intervals: [],

      saved_name: '',
      saved_description: '',
      saved_category: '',
      saved_intervals: [],
    }
  },
  created() {
    this.getScale();
  },
  computed: {
    isFormValid() {
      return !this.loading
      && this.scale_info_changed
      && this.current_name.trim()
      && this.current_category.trim()
      && this.current_intervals != [];
    },
    instrumentRedirectPath() {
      const instrument = "guitar";
      const tuning = "standard";
      return `/instrument/${instrument}/${tuning}/${this.scale_id}`;
    }
  },
  methods: {
    redirectToInstrument() {
      this.$router.push(this.instrumentRedirectPath);
    },
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
			this.current_intervals.splice(index, 1);
    },
    resetForm() {
      this.current_name = this.saved_name;
      this.current_description = this.saved_description;
      this.current_category = this.saved_category;
      this.current_intervals = [...this.saved_intervals];
      this.scale_info_changed = false;
    },
    async getScale() {
			this.loading = true;
			await api.get(`/scale/${this.scale_id}`, { 
				headers: { 
					'Content-Type': 'application/x-www-form-urlencoded',
					'Authorization': `Bearer ${useAuthStore().token}`
				}
			})
			.then(response => {
				this.error_message = '';
				this.no_content_message = '';

				if (response.status == 204) {
					console.log(response.data);
					this.no_content = true;
					this.no_content_message = 'Ничего не найдено!';
					return;
				};

				let scale = response.data;
				if (useAuthStore().isAuthenticated && useAuthStore().user && response.data["owner_id"] == useAuthStore().user._id) {
						this.is_my_scale = true;
				};

				this.saved_name = scale["name"];
				this.saved_description = scale["description"];
				this.saved_category = scale["category"];
				this.saved_intervals = [...scale["intervals"]];

        this.current_name = this.saved_name;
        this.current_description = this.saved_description;
        this.current_category = this.saved_category;
        this.current_intervals = [...this.saved_intervals];
			})
			.catch(error => {
				console.error(error);
				this.error_message = error.response?.data?.detail | "Произошла ошибка";
				if (error.response?.status == 403) {
						this.no_content = true;
						this.no_content_message = 'Просмотр этой гаммы запрещен для текущего пользователя';
				};
			})
			.finally(() => {
				this.loading = false;
			});
    },
    async submitScale() {
			this.loading = true;
      const data = {
        name: this.current_name.trim(),
        description: this.current_description.trim(),
        category: this.current_category.trim(),
        intervals: this.current_intervals
      };
      await api.patch(`/scale/${this.scale_id}`, 
        data, {
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${useAuthStore().token}`
        }
      })
      .then (response => {
        this.error_message = '';
        this.scale_info_changed = false;

        this.saved_name = this.current_name;
        this.saved_description = this.current_description;
        this.saved_category = this.current_category;
        this.saved_intervals = [...this.current_intervals];
      })
      .catch (error => {
        this.error_message = error.response?.data?.detail | "Произошла ошибка";
        console.error(error);
      })
			.finally(() => {
				this.loading = false;
			});
    },
    async deleteScale() {
			this.loading = true;
      await api.delete(`/scale/${this.scale_id}`)
      .then (response => {
        this.error_message = '';
        this.scale_info_changed = false;
      })
      .catch (error => {
        this.error_message = error.response?.data?.detail | "Произошла ошибка";
        console.error(error);
      })
			.finally(() => {
				this.loading = false;
			});
    }
  }
}
</script>

<style scoped>
.modal-content {
  border-top: 4px solid #4da6ff;
}

.remove-button {
  background-color: white;
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

.remove-button:hover {
  color: rgb(200, 0, 0);
  border-color: rgb(200, 0, 0);
}

.scale-name {
  color: var(--dark-blue);
  margin: 0;
  font-size: 1.5rem;
}

.form-label {
  font-size: 1.2rem;
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
</style>