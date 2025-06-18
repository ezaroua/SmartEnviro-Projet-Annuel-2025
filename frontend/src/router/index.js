import { createRouter, createWebHistory } from 'vue-router'

/* Layouts */
import PublicLayout      from '@/layouts/PublicLayout.vue'
import DashboardLayout   from '@/layouts/DashboardLayout.vue'
import AdminLayout       from '@/layouts/AdminLayout.vue'

/* Pages publiques */
import HomeView          from '@/views/HomeView.vue'
import LoginView         from '@/views/LoginView.vue'
import RegisterView      from '@/views/RegisterView.vue'

/* Pages citoyen */
import DashboardCitizen  from '@/views/citizen/DashboardView.vue'
import ProfileView       from '@/views/ProfileView.vue'

/* Pages admin */
import DashboardAdmin    from '@/views/admin/AdminDashboard.vue'

const routes = [
  // Pages publiques
  {
    path: '/',
    component: PublicLayout,
    children: [
      { path: '', name: 'home', component: HomeView },
      { path: 'login', name: 'login', component: LoginView },
      { path: 'register', name: 'register', component: RegisterView }
    ]
  },

  // Dashboard citoyen
  {
    path: '/dashboardCitizen',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'citizen' },
    children: [
      { path: '', name: 'dashboard-citizen', component: DashboardCitizen },
      { path: 'profile', name: 'citizen-profile', component: ProfileView } 
    ]
  },

  // Dashboard admin
  {
    path: '/dashboardAdmin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '', name: 'dashboard-admin', component: DashboardAdmin },
      { path: 'profile', name: 'admin-profile', component: ProfileView } 
    ]
  },

  {
  path: '/alerts',
  name: 'alerts',
  component: () => import('@/views/citizen/AlertsView.vue'),
  meta: { requiresAuth: true, role: 'citizen' }
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/* Sécurité et redirection selon le rôle */
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role') // "1" = admin, "2" = citizen

  if (to.meta.requiresAuth && !token) return next('/login')
  if (to.meta.role === 'admin' && role !== '1') return next('/dashboardCitizen')
  if (to.meta.role === 'citizen' && role !== '2') return next('/dashboardAdmin')

  next()
})

export default router