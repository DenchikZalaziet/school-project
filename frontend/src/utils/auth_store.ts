import { defineStore } from 'pinia';
import api from '@/utils/axios';
import router from '@/utils/router';

const setAxiosToken = (token: string) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};


export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error_message: '',
  }),
  actions: {
    async setup() {
      this.loading = true;
      this.error_message = '';

      await api.get('/user/me', {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded', 
          'Authorization': `Bearer ${this.token}`
        }
      })
      .then(response => {
        this.user = response.data;
      })
      .catch(error => {
         if (error.response?.data?.detail) {
          this.error_message = error.response.data.detail;
        } else {
          this.error_message = "Произошла ошибка";
        };
        console.error(error);
        this.token = null;
       })
      .finally(() => {
        setAxiosToken(this.token);
        this.loading = false;
      });
    },
    async login(username: string, password: string) {
      this.loading = true;
      this.error_message = '';
      
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      await api.post('/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded'}
      })
      .then(response => {
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        setAxiosToken(this.token);
        this.fetchUser();
        router.push('/');
      })
      .catch (error => {
        if (error.response?.data?.detail) {
          this.error_message = error.response.data.detail;
        } else {
          this.error_message = "Произошла ошибка";
        };
        console.error(error);
      })
      .finally(() => {
        this.loading = false;
      });
    },
    async register(username: string, password: string) {
      this.loading = true;
      this.error_message = '';

      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      await api.post('/auth/register', params, {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded' 
        }
      })
      .then(response => {
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        setAxiosToken(this.token);
        this.fetchUser();
        router.push('/');
      })
      .catch (error => {
        if (error.response?.data?.detail) {
          this.error_message = error.response.data.detail;
        } else {
          this.error_message = "Произошла ошибка";
        };
        console.error(error);
      })
      .finally(() => {
        this.loading = false;
      });
    },
    logout() {
      this.error_message = '';
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    },
    changeToken(token: string) {
      if (token) {
        this.token = token;
      };
      setAxiosToken(token);
    },
    async fetchUser() {
      if (this.token == null) {return};
      this.loading = true;
      this.error_message = '';

      await api.get('/user/me', {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Bearer ${this.token}`
        }
      })
      .then(response => {
        this.user = response.data;
      })
      .catch(error => {
        if (error.response?.data?.detail) {
            this.error_message = error.response.data.detail;
        } else {
            this.error_message = "Произошла ошибка";
        };
        console.error(error);
      })
      .finally(() => {
        this.loading = false;
      });
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    username: (state) => state.user?.username,
    description: (state) => state.user?.description,
  }
});
