<template>
  <div class="d-flex min-vh-100">
    <aside class="bg-dark text-white p-3 d-flex flex-column" style="width:240px; min-height: 100%;">
      <h4 class="text-center mb-4">Admin</h4>
      <ul class="nav flex-column gap-2">
        <li><router-link class="nav-link text-white" to="/dashboardAdmin">Dashboard</router-link></li>
         <li><router-link class="nav-link text-white" to="/dashboardAdmin/profile">Profil</router-link></li>
        <li><router-link class="nav-link text-white" to="/dashboardAdmin/users">Utilisateurs</router-link></li>
        <li><router-link class="nav-link text-white" to="/admin/stations">Stations</router-link></li>
        <li><router-link class="nav-link text-white" to="/admin/thresholds">Seuils</router-link></li>
        <li><router-link class="nav-link text-white" to="/admin/logs">Logs</router-link></li>
        <li class="mt-auto">
          <button class="btn btn-outline-light w-100" @click="logout">Déconnexion</button>
        </li>
      </ul>
    </aside>

    <div class="flex-fill">
      <nav class="navbar navbar-dark bg-dark shadow-sm">
        <span class="navbar-brand ms-3">Console d’administration</span>
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
