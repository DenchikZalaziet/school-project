import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 5000,
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
