import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: import.meta.env.VITE_API_TIMEOUT,
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

export default api;
