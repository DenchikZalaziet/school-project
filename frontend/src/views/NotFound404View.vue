<template> 
  <div class="container mb-5 p-4">
    <div class="empty-state row text-center justify-content-center py-5">
      <h1>404 - Страница не найдена!</h1>
      <hr style="width: 70%;">
      <h3>Страница, которую вы ищите, не существует</h3>
      <router-link to="/">
        <button class="btn btn-primary btn-home mt-4">На главную</button>
      </router-link>
    </div>
  </div>
</template>


<script setup>
</script>

<script>
export default {
  name: '404 View',
}
</script>

<style scoped>
.empty-state {
  color: var(--dark-blue);
  background-color: var(--light-blue);
  border-radius: 10px;
  margin-top: 2rem;
  border-top: 4px solid #4da6ff;
}
</style>