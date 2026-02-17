<template>
  <footer class="footer py-4">
    <div class="container text-center">
      <div class="mb-1">
        <img src="../assets/logo.png" alt="Logo" class="footer-logo" style="height: 60px;">
      </div>
      
      <ul class="nav justify-content-center mb-3">
        <router-link :to="`/`" class="footer-link">
          <a class="nav-link px-3 text-white">Главная</a>
        </router-link>
        <router-link :to="`/scales/`" class="footer-link">
          <a class="nav-link px-3 text-white">Гаммы</a>
        </router-link>
      </ul> 
      
      <a href="#top" class="d-block my-2 text-white nav-link top-link footer-link">Вернуться наверх ↑</a>
      <p class="mb-0 text-white-50">2026 Школьный проект по информатике</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
footer {
	margin-top: auto;
  background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
  border-top: 3px solid var(--primary-blue);
}

.footer-link { 
  text-decoration: none; 
}

.top-link {
  font-size: 1.1rem;
}

.nav-link {
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: var(--primary-blue) !important;
  transform: translateY(-2px);
}

.text-white-50 {
  color: rgba(255, 255, 255, 0.7) !important;
}
</style>
