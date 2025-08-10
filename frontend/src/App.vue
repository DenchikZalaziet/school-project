<template>
  <div id="app">
    <h1>{{ message }}</h1>
    <button @click="testRegister">Register</button>
    <button @click="testLogin">Login</button>
    <h1>{{ messageLogin }}</h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
     message: "",
     messageLogin: "No token",
    };
  },
  methods: {
    async testRegister() {
      const formData = new URLSearchParams();
      formData.append('username', "example");
      formData.append('password', "example");

      const response = await axios.post(`http://127.0.0.1:8000/auth/register`, formData,
      { headers: {'Content-Type': 'application/x-www-form-urlencoded'}});
      this.messageLogin = response;
      console.log(response);
    },
    async testLogin() {
      const formData = new URLSearchParams();
      formData.append('username', "example");
      formData.append('password', "example");

      const response = await axios.post(`http://127.0.0.1:8000/auth/login`, formData,
      { headers: {'Content-Type': 'application/x-www-form-urlencoded'}});
      this.messageLogin = response;
      console.log(response);
    }
  },
  async mounted() {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/`);
      this.message = response.data.message;
    } catch {
     this.message = "Something went wrong";
    }
  }
};
</script>

<style>
</style>
