<template>
  <footer class="footer mt-auto py-5 text-white">
    <div class="container">
      <div class="row align-items-center">
        
        <div class="col-md-4 text-center text-md-start mb-4 mb-md-0">
          <img src="../assets/logo.png" alt="Logo" class="footer-logo mb-2">
          <h5 class="fw-bold mb-1">PolyFret</h5>
        </div>

        <div class="col-md-4 text-center mb-4 mb-md-0">
          <ul class="nav justify-content-center">
            <li class="nav-item">
              <router-link to="/" class="nav-link footer-nav-link px-3">Главная</router-link>
            </li>
            <li class="nav-item">
              <router-link :to="{path: '/scales/', query: {page: 1}}" class="nav-link footer-nav-link px-3">Гаммы</router-link>
            </li>
          </ul>
        </div>

        <div class="col-md-4 text-center text-md-end">
          <a href="#top" class="back-to-top text-decoration-none">
            <span class="me-2">Наверх</span>
            <div class="arrow-circle">↑</div>
          </a>
        </div>

      </div>
      
      <div class="border-top border-secondary mt-4 pt-3 text-center">
        <p class="small text-white-50 mb-0">2026 Школьный проект по информатике.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: linear-gradient(180deg, #2c3e50 0%, #1a252f 100%);
  border-top: 5px solid #0d6efd;
}

.footer-logo {
  height: 50px;
  opacity: 0.8;
}

.footer-nav-link {
  color: rgba(255, 255, 255, 0.8) !important;
  font-weight: 500;
  transition: color 0.2s ease;
}

.footer-nav-link:hover {
  color: #0d6efd !important;
}

.back-to-top {
  color: white;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  transition: opacity 0.2s ease;
}

.back-to-top:hover {
  opacity: 0.8;
}

.arrow-circle {
  width: 35px;
  height: 35px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}

.back-to-top:hover .arrow-circle {
  background: #0d6efd;
}

.text-white-50 {
  color: rgba(255, 255, 255, 0.5) !important;
}
</style>
