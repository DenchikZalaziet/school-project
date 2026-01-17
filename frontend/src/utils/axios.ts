import axios from 'axios';
import { env } from '@/utils/env.js';

const api = axios.create({
  baseURL: env.API_BASE_URL,
  timeout: env.API_TIMEOUT,
});

// api.interceptors.response.use(
//   response => response,
//   error => {
//     const status = error.response?.status;

//     if (status == 401) {
//       window.location.href = '/login';
//     }

//     return Promise.reject(error);
//   }
// );

export { api };
