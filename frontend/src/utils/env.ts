export const env = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  API_TIMEOUT: import.meta.env.VITE_API_TIMEOUT || 5000,
  DEBUG: ['true', '1'].includes(import.meta.env.VITE_DEBUG?.toLowerCase()),
};
