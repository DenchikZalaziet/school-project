<template>
<div class="scales-page">

    <div class="header-controls mb-4">
      <h1 class="page-title">Мои гаммы</h1>
      <div class="controls d-flex align-items-center">
        <div class="search-box">
          <input type="text" class="form-control" placeholder="Искать по названию..." v-model="searchQuery">
        </div>
      </div>
    </div>

    <div class="scales-container">
      <div class="row row-cols-1 row-cols-md-2 g-4">
        <div class="col" v-for="scale in paginatedScales" :key="scale._id">
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
      
      <div v-if="paginatedScales.length === 0" class="empty-state text-center py-5">
        <i class="fas fa-music fa-3x mb-3"></i>
        <h4>Ничего не найдено!</h4>
      </div>
    </div>

    <nav v-if="totalPages > 1" class="mt-4">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="changePage(currentPage - 1)">Предыдущая</button>
        </li>
        <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
          <button class="page-link" @click="changePage(page)">{{ page }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="changePage(currentPage + 1)">Следующая</button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import Scales from './Scales.vue'
import api from '@/utils/axios'

const pageLength = 10

export default {
  extends: Scales,
  methods: {
    async loadScalesPage() {
      await api.get('/user/me/scale', {
        params: {
            length: pageLength,
            page: this.currentPage,
            query: this.searchQuery
        }
      })
      .then (response => {
        this.totalPages = response.data["pages"]
        this.paginatedScales = response.data["scales"]
      })
      .catch (error => {
        console.log(error)
      })
    }
  }
}
</script>


<style scoped>
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
</style>