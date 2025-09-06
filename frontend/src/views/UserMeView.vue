<template>
  <Header></Header>

  <body class="body">

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
        placeholder="Имя"
        v-model="current_username"
        maxlength="20"
        @change="user_info_changed = true"
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


  <div class="scales-page">

    <div class="header-controls mb-4">
      <h1 class="page-title">Мои гаммы</h1>
      <div class="controls d-flex align-items-center">
        <div class="search-box">
          <input type="text" class="form-control" placeholder="Искать по названию..." v-model="search_query">
        </div>
      </div>
    </div>

    <div class="scales-container">
      <div class="row row-cols-1 row-cols-md-2 g-4">
        <div class="col" v-for="scale in paginated_scales" :key="scale.id">
          <router-link :to="`/scales/${scale._id}/`" class="scale-link">
            <div class="scale-card card h-100">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h3 class="scale-name">{{ scale.name }}</h3>
                <span class="badge bg-primary">{{ scale.category ? scale.category : "Нет категории" }}</span>
              </div>
              <div class="card-body">
                <p class="scale-description">{{ scale.description ? scale.description : "Нет описания" }}</p>
              </div>
            </div>
          </router-link>
        </div>
      </div>
      
      <div v-if="paginated_scales.length === 0" class="empty-state text-center py-5">
        <i class="fas fa-music fa-3x mb-3"></i>
        <h4>Ничего не найдено!</h4>
      </div>
    </div>

    <nav v-if="total_pages > 1" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: current_page === 1 }">
          <button class="page-link" @click="changePage(current_page - 1)">Предыдущая</button>
        </li>
        <li class="page-item" v-for="page in total_pages" :key="page" :class="{ active: current_page === page }">
          <button class="page-link" @click="changePage(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: current_page === total_pages }">
          <button class="page-link" @click="changePage(current_page + 1)">Следующая</button>
        </li>
      </ul>
    </nav>
  </div>
  </body>
</template>

<script setup>
import Header from '@/components/Header.vue'
import { useAuthStore } from '@/utils/auth_store';

const authStore = useAuthStore()
</script>

<script>
import api from '@/utils/axios';

const pageLength = 10
export default {
  name: 'My Profile View',
  data() {
    return {
        error_message: '',

        selected_category: "all",
        search_query: "",
        current_page: 1,
        total_pages: 1,
        paginated_scales: [],

        current_username: useAuthStore().username,
        current_description: useAuthStore().description,
        user_info_changed: false
    }
  },
  methods: { 
    changePage(page) {
        if (page <= this.totalPages && page > 0) {
            this.currentPage = page
            loadPublicScalesPage()
        }
    },
    async loadPublicScalesPage() {
      await api.get('/user/me/scale', {
        params: {
            length: pageLength,
            page: this.current_page,
            query: this.search_query
        },
        headers: { 
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `Bearer ${useAuthStore().token}`
        }
      })
      .then (response => {
        this.total_pages = response.data["pages"]
        this.paginated_scales = response.data["scales"]
      })
      .catch (error => {
        console.log(error)
      })
    },
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
    searchQuery() {
      this.loadPublicScalesPage()
    }
  },
  created() {
    this.loadPublicScalesPage()
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

.scales-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header-controls {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.page-title {
  color: var(--dark-blue);
  margin-bottom: 0;
}

.controls {
  flex-wrap: wrap;
  gap: 1rem;
}

.category-filter {
  min-width: 180px;
}

.search-box {
  min-width: 250px;
}

.scale-card {
  border: 2px solid var(--border-blue);
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.scale-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  background-color: var(--light-blue);
  border-bottom: 2px solid var(--border-blue);
  padding: 1rem 1.25rem;
}

.badge {
  background-color: var(--primary-blue);
  font-size: 0.9rem;
  padding: 0.5em 0.75em;
}

.card-body {
  padding: 1.25rem;
}

.scale-name {
  color: var(--dark-blue);
  margin: 0;
  font-size: 1.5rem;
}

.scale-description {
  color: #444;
  line-height: 1.6;
}

.pagination .page-item.active .page-link {
  background-color: var(--primary-blue);
  border-color: var(--primary-blue);
}

.page-link {
  color: var(--dark-blue);
}

.page-link:hover {
  color: var(--primary-blue);
}

.empty-state {
  color: var(--dark-blue);
  background-color: var(--light-blue);
  border-radius: 10px;
  margin-top: 2rem;
}

.scale-link {
  text-decoration: none;
  display: block;
  color: inherit;
}

.scale-card {
  cursor: pointer;
  position: relative;
}

.scale-link:hover .scale-card {
  transform: translateY(-7px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  border-color: var(--primary-blue);
}

.scale-card {
  transition: all 0.3s ease, border-color 0.2s ease;
}

@media (max-width: 768px) {
  .header-controls {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .controls {
    width: 100%;
  }
  
  .category-filter,
  .search-box {
    width: 100%;
  }
}
</style>