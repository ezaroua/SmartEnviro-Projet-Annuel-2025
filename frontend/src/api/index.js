import axios from "axios";
import { useAuthStore } from "./auth";

console.log(import.meta.env.VITE_API_URL);

// Créer une instance Axios avec l'URL de base
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  // 'https://smartenviro-production.up.railway.app/', // TODO: Should be get from the meta.env.VITE_API_URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Intercepteur de requête pour ajouter le token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur pour gérer les erreurs d'authentification
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Si erreur 401 (non authentifié) et pas déjà tenté de refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const authStore = useAuthStore();
        const refreshed = await authStore.refreshToken();

        if (refreshed) {
          // Retenter la requête originale avec le nouveau token
          const token = localStorage.getItem("token");
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        const authStore = useAuthStore();
        authStore.logout();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
