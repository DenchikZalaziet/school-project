<template>
<Header></Header>
<div class="container mb-5">
    <div id="app">

        <div class="container mb-5 p-4">
            <div v-if="no_content" class="empty-state text-center py-5">
                <i class="fas fa-music fa-3x mb-3"></i>
                <h2>{{ no_content_message }}</h2>
            </div>

            <div v-else class="row justify-content-center">
                <div class="col-md-10">
                    <div class="mb-4">
                        <label for="scaleName" class="form-label fw-bold">Название</label>
                        <input type="text"
                            class="form-control form-control-lg custom-input scale-name" 
                            id="scaleName" 
                            @change="scale_info_changed = true"
                            v-model="current_name"
                            placeholder="Имя"
                            :disabled="!is_my_scale">
                    </div>

                    <div class="mb-4">
                        <label for="scaleCategory" class="form-label fw-bold">Категория</label>
                        <div class="by-1">
                            <span class="badge rounded-pill mx-2">{{ current_category }}</span>
                        </div>
                    </div>

                    <div class="mb-4">
                        <label for="scaleDescription" class="form-label fw-bold">Описание</label>
                        <textarea class="form-control custom-input scale-description" 
                            id="scaleDescription" 
                            rows="3"
                            @change="scale_info_changed = true"
                            v-model="current_description"
                            placeholder="Описание"
                            :disabled="!is_my_scale">
                        </textarea>
                    </div>

                    <div class="mb-4">
                        <label class="form-label fw-bold">Интервалы</label>
                        <div class="intervals-container">
                            <form @submit.prevent="submitScale">
                            <div v-for="(interval, index) in current_intervals" :key="index" class="interval-item p-3 mb-2 rounded">
                            <div class="d-flex align-items-center justify-content-between">
                                <span v-if="!is_my_scale" class="interval-number fs-5 fw-bold">{{ interval }}</span>
                                
                                <div v-else class="d-flex align-items-center gap-2">
                                <input type="number" 
                                        class="form-control interval-input" 
                                        v-model.number="current_intervals[index]"
                                        min="0" 
                                        max="12"
                                        @change="scale_info_changed = true"
                                        style="width: 80px">
                                <span class="text-nowrap">полутонов</span>
                                </div>
                                
                                <button v-if="is_my_scale" 
                                        type="button" 
                                        class="btn btn-outline-danger btn-sm"
                                        @click="removeInterval(index); scale_info_changed = true">
                                <i class="fas fa-times"></i>
                                X
                                </button>
                            </div>
                            </div>
                            
                            <button v-if="is_my_scale" 
                                    type="button" 
                                    class="btn btn-primary mt-2"
                                    @click="addInterval(1); scale_info_changed = true">
                            <i class="fas fa-plus me-1"></i> Добавить интервал
                            </button>

                            <div v-if="is_my_scale" class="d-flex gap-2 justify-content-end mt-4">
                                <button type="submit" class="btn btn-success" :disabled="!isFormValid">Сохранить</button>
                            </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import api from '@/utils/axios';
import { useAuthStore } from '@/utils/auth_store';
</script>

<script>
export default {
  name: 'Scale View',
  data() {
    return {
      error_message: '',
      no_content: false,
      no_content_message: '',

      scale_info_changed: false,

      scale_id: this.$route.params.scale_id,
      is_my_scale: false,

      current_name: '',
      current_description: '',
      current_category: '',
      current_intervals: []
    }
  },
  methods: {
    addInterval(value) {
        this.current_intervals.push(value);
    },
    removeInterval(index) {
        this.current_intervals.splice(index, 1)
    },
    async getScale() {
        await api.get(`/scale/${this.scale_id}`, 
        { headers: { 
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `Bearer ${useAuthStore().token}`
         }
        })
        .then(response => {
            this.error_message = ''
            this.no_content_message = ''
            if (response.status == 204) {
                console.log(response.data)
                this.no_content = true
                this.no_content_message = 'Ничего не найдено!'
                return
            }
            let scale = response.data
            if (response.data["owner_id"] == useAuthStore().user._id) {
                this.is_my_scale = true
            }
            this.current_name = scale["name"]
            this.current_description = scale["description"]
            this.current_category = scale["category"]
            this.current_intervals = scale["intervals"]
        })
        .catch(error => {
            console.log(error)
            this.error_message = error.response?.data?.detail | "Произошла ошибка"
            if (response.status == 402) {
                this.no_content = true
                this.no_content_message = 'Просмотр приватной гаммы запрещен'
            }
        })
    },
    async submitScale() {
      const formData = new FormData()
      formData.append("name", this.current_name)
      formData.append("description", this.curren_description)
      formData.append("category", this.current_category)
      formData.append("intervals", this.current_intervals)

      await api.patch(`/scale/${this.scale_id}`, 
        formData, {
        headers: { 
            "Content-Type": "multipart/form-data"
        }
      })
      .then (response => {
        this.error_message = ''
        this.scale_info_changed = false
      })
      .catch (error => {
        this.error_message = error.response?.data?.detail | "Произошла ошибка"
        console.log(error)
      })
    },
    async deleteScale(){

    }
  },
  computed: {
    isFormValid() {
        return this.scale_info_changed
    }
  },
  created() {
    this.getScale()
  }
}
</script>

<style scoped>
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
}

.interval-input {
  border: 1px solid var(--border-blue);
  background-color: white;
  color: var(--dark-blue);
}
</style>