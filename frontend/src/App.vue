<template>
  <div id="app" class="app-container">
    <main class="main-content">
      <RouterView/>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Footer from './components/Footer.vue';
</script>

<script>
export default {
    name: 'App',
}
</script>

<style>
:root {
  --primary-blue: #4da6ff;
  --dark-blue: #2c7db6;
  --light-blue: #e0f7ff;
  --border-blue: #c1e3ff;
}

* {
  scrollbar-width: thin;
  scrollbar-color: var(--primary-blue) #f1f1f1;
}

html {
  scroll-behavior: smooth;
}
</style>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1 0 auto;
}
</style>