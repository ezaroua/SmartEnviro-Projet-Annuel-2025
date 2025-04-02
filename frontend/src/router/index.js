import { createRouter, createWebHistory } from 'vue-router'

// Importer d'abord une seule vue
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  
  {
    path: '/login',
    name: 'login',
    component: { template: '<div>Page de connexion</div>' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router