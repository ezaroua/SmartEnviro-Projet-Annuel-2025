<template>
  <div class="d-flex">
    <!-- Sidebar -->
    <aside class="bg-primary text-white p-3 vh-100" style="width:220px">
      <h4 class="text-center mb-4">Menu</h4>
      <ul class="nav flex-column gap-2">
        <li><router-link class="nav-link text-white" to="/dashboardCitizen">Tableau de bord</router-link></li>
        <li><router-link class="nav-link text-white" to="/alerts">Alertes</router-link></li>
        <li><router-link class="nav-link text-white" to="/dashboardCitizen/profile">Profil</router-link></li>
        <li class="mt-auto">
          <button class="btn btn-outline-light w-100" @click="logout">Déconnexion</button>
        </li>
      </ul>
    </aside>

    <!-- Main -->
    <div class="flex-fill">
      <nav class="navbar navbar-dark bg-primary shadow-sm">
        <span class="navbar-brand ms-3">Citoyen</span>
      </nav>
      <main class="p-4"><router-view/></main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>
