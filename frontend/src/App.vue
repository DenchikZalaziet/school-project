<template>
  <div id="app">
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
     message: ""
    };
  },
  async mounted() {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api`);
      this.message = response.data.message;
    } catch {
     this.message = "Something went wrong"
    }
  }
};
</script>

<style>
</style>
