<template>
  <MusicBackground />
  <Header />
  <div class="container mb-5 p-4">
    <div v-if="no_content" class="empty-state text-center py-5 shadow-sm">
      <h2 class="mb-0">{{ no_content_message }}</h2>
    </div>

    <div v-else class="row justify-content-center">
      <form @submit.prevent="submitScale" class="col-md-10">
        <h2 class="mb-4">{{ is_my_scale ? 'Редактирование гаммы' : 'Просмотр гаммы' }}</h2>
        
        <div v-if="error_message" class="alert alert-danger mb-4">{{ error_message }}</div>

        <div class="mb-4">
          <label for="scaleName" class="form-label fw-bold text-secondary text-uppercase small tracking-wider">Название</label>
          <input type="text" class="form-control form-control-lg custom-input scale-name" 
            id="scaleName" @input="scale_info_changed = true" v-model="current_name" maxlength="50"
            placeholder="Имя" :disabled="!is_my_scale">
        </div>

        <div class="mb-4">
          <label class="form-label fw-bold text-secondary text-uppercase small tracking-wider">Категория</label>
          <div class="py-2">
            <span class="badge rounded-pill px-4 py-2 fs-6 shadow-sm custom-category-badge">
              {{ current_category }}
            </span>
          </div>
        </div>

        <div class="mb-4">
          <label for="scaleDescription" class="form-label fw-bold text-secondary text-uppercase small tracking-wider">Описание</label>
          <textarea class="form-control custom-input scale-description" 
            id="scaleDescription" rows="3" @input="scale_info_changed = true" maxlength="70"
            v-model="current_description" placeholder="Описание" :disabled="!is_my_scale"></textarea>
        </div>

        <div class="mb-4">
          <label class="form-label fw-bold text-secondary text-uppercase small tracking-wider">Интервалы</label>
          <div class="intervals-container">
            <div v-for="(interval, index) in current_intervals" :key="index" class="interval-item p-3 mb-2 rounded shadow-sm">
              <div class="d-flex align-items-center justify-content-between">
                <div v-if="is_my_scale" class="d-flex align-items-center gap-2">
                  <input type="number" class="form-control interval-input" v-model.number="current_intervals[index]"
                    min="0" max="12" @input="scale_info_changed = true" style="width: 80px">
                  <span class="text-nowrap fs-5">{{ intervalName(interval) }}</span>
                </div>
                <span v-else class="fs-5">{{ interval }} {{ intervalName(interval) }}</span>
                
                <button v-if="is_my_scale" type="button" class="btn btn-outline-danger btn-sm border-0"
                  @click="removeInterval(index); scale_info_changed = true" :disabled="current_intervals.length <= 1">✕</button>
              </div>
            </div>
              
            <div class="d-flex align-items-center gap-3 mt-3">
              <button v-if="is_my_scale" type="button" class="btn btn-primary px-4 rounded-pill" @click="addInterval(1); scale_info_changed = true">+ Добавить</button>
              <ScalePlayer :intervals="current_intervals" />
            </div>

            <div class="d-flex flex-wrap gap-2 justify-content-between mt-5 border-top pt-4">
              <button type="button" class="btn btn-outline-primary rounded-pill px-4" @click="handleInstrumentRedirect">Отобразить на инструменте</button>

              <div v-if="is_my_scale" class="d-flex gap-2">
                <div @click="handleDisabledSaveClick" class="d-inline-block">
                  <button type="submit" class="btn btn-success form-btn rounded-pill px-4" :disabled="!isFormValid">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
                    {{ loading ? '...' : 'Сохранить' }}
                  </button>
                </div>
                <button type="button" class="btn btn-outline-secondary rounded-pill px-4" @click="resetForm" :disabled="!scale_info_changed">Сбросить</button>
                <button type="button" class="btn btn-danger rounded-pill px-4" @click="triggerDeleteModal">Удалить</button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>

    <div class="modal fade" id="successModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-success text-white border-0"><h5 class="modal-title">Успешно!</h5></div>
          <div class="modal-body py-4 text-center fs-5">Изменения сохранены.</div>
          <div class="modal-footer border-0"><button class="btn btn-success rounded-pill px-4" data-bs-dismiss="modal">Ок</button></div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="deleteModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-danger text-white border-0"><h5 class="modal-title">Удаление</h5></div>
          <div class="modal-body py-4">Вы действительно хотите безвозвратно удалить эту гамму?</div>
          <div class="modal-footer border-0">
            <button class="btn btn-danger rounded-pill px-4" data-bs-dismiss="modal" @click="deleteScale">Да, удалить</button>
            <button class="btn btn-outline-secondary rounded-pill px-4" data-bs-dismiss="modal">Отмена</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="hintModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-warning text-dark border-0"><h5 class="modal-title">Внимание</h5></div>
          <div class="modal-body py-4">{{ hint_message }}</div>
          <div class="modal-footer border-0"><button class="btn btn-dark rounded-pill px-4" data-bs-dismiss="modal">Понятно</button></div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="saveBeforeRedirectModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header border-0"><h5 class="modal-title fw-bold">Сохранить изменения?</h5></div>
          <div class="modal-body">Вы внесли правки. Сохранить их перед переходом?</div>
          <div class="modal-footer border-0">
            <button class="btn btn-primary rounded-pill px-4 " data-bs-dismiss="modal" @click="submitScale().then(redirectToInstrument)">Сохранить</button>
            <button class="btn btn-outline-secondary rounded-pill px-4" data-bs-dismiss="modal" @click="resetForm(); redirectToInstrument()">Нет</button>
          </div>
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
  name: 'ScaleByIdView',
  components: {
    Header,
    MusicBackground,
    ScalePlayer
  },
  data() {
    return {
      error_message: '', 
      hint_message: '', 
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
  created() { this.getScale(); },
  computed: {
    isFormValid() {
      return !this.loading && this.scale_info_changed && this.current_name.trim() !== '' && this.current_intervals.length > 0; 
    },
  
    instrumentRedirectPath() { 
      return `/instrument/${this.scale_id}/`;
    }
  },
  methods: {
    handleDisabledSaveClick() {
      if (!this.isFormValid && !this.loading) {
        this.hint_message = !this.scale_info_changed ? "Изменений не обнаружено." : "Название не может быть пустым.";
        new Modal(document.getElementById('hintModal')).show();
      }
    },

    triggerDeleteModal() { new Modal(document.getElementById('deleteModal')).show(); },

    handleInstrumentRedirect() {
      if (this.scale_info_changed && this.is_my_scale) {
        new Modal(document.getElementById('saveBeforeRedirectModal')).show();
      } else { this.redirectToInstrument(); }
    },

    redirectToInstrument() { this.$router.push(this.instrumentRedirectPath); },

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
      this.current_name = this.saved_name; this.current_description = this.saved_description;
      this.current_category = this.saved_category; this.current_intervals = [...this.saved_intervals];
      this.scale_info_changed = false;
    },

    async getScale() {
      this.loading = true;
      await api.get(`/scale/${this.scale_id}`, { 
        headers: { 'Authorization': `Bearer ${useAuthStore().token}` }
      })
      .then(result => {
        if (result.status == 204) { this.no_content = true; this.no_content_message = 'Гамма не найдена!'; return; }
        const s = result.data;
        if (useAuthStore().isAuthenticated && useAuthStore().user?._id == s.owner_id) this.is_my_scale = true;
        this.saved_name = s.name; this.saved_description = s.description; this.saved_category = s.category; this.saved_intervals = [...s.intervals];
        this.resetForm();
      })
      .catch(error =>  { 
        this.error_message = "Ошибка загрузки"; 
      })
      .finally(() => { 
        this.loading = false; 
      });
    },

    async submitScale() {
      this.loading = true;
      await api.patch(`/scale/${this.scale_id}`, {
        name: this.current_name.trim(), description: this.current_description.trim(),
        category: this.current_category, intervals: this.current_intervals
      }, { 
        headers: { 'Authorization': `Bearer ${useAuthStore().token}` }
      })
      .then(response => {
        this.saved_name = this.current_name; this.saved_intervals = [...this.current_intervals];
        this.scale_info_changed = false;
        new Modal(document.getElementById('successModal')).show();
      })
      .catch(error => { 
        this.error_message = "Ошибка сохранения";
      })
      .finally(() => { 
        this.loading = false; 
      });
    },

    async deleteScale() {
      await api.delete(`/scale/${this.scale_id}`, { 
        headers: { 'Authorization': `Bearer ${useAuthStore().token}` }
      })
      .then(response => { 
        this.$router.push('/scales');
      })
      .catch(error => { 
        this.error_message = "Ошибка удаления"; 
      });
    }
  }
}
</script>

<style scoped>
.custom-input { 
  border: 1px solid var(--border-blue); 
  background-color: var(--light-blue); 
}

.interval-item { 
  border-left: 4px solid #007bff; 
  background-color: #f8f9fa; 
}

.badge { 
  background-color: #007bff; 
}

.form-btn { 
  min-width: 120px; 
}

.empty-state { 
  border-top: 4px solid #4da6ff; 
  background: white; 
  border-radius: 12px; 
}
</style>
