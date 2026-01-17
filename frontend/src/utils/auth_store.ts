import { defineStore } from 'pinia';
import { env } from '@/utils/env.js';
import { api } from '@/utils/axios.js';
import router from '@/utils/router.js';

const setAxiosToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') as string),
    token: localStorage.getItem('token') ?? null,
    loading: false,
    error_message: '',
  }),
  actions: {
    async setup() {
      await this.fetchUser();
    },

    async login(username: string, password: string) {
      this.loading = true;
      this.error_message = '';
      
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      return api.post('/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded'}
      })
      .then(response => {
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token? this.token : "");
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
        if (env.DEBUG) {
          console.error(error);
        };
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

      return api.post('/auth/register', params, {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded' 
        }
      })
      .then(response => {
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token? this.token : "");
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
        if (env.DEBUG) {
          console.error(error);
        };
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

      return api.get('/user/me', {
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
        if (env.DEBUG) {
          console.error(error);
        };
        this.token = null;
        this.user = null;
       })
      .finally(() => {
        setAxiosToken(this.token);
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
