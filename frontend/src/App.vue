<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <a class="navbar-brand" href="#" @click.prevent="currentPage = 'home'">Smart City App</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="currentPage = 'login'">Connexion</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="currentPage = 'register'">Inscription</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    
    <HomeView v-if="currentPage === 'home'" @navigate="currentPage = $event"/>
    <LoginView v-if="currentPage === 'login'" @navigate="currentPage = $event"/>
    <RegisterView v-if="currentPage === 'register'" @navigate="currentPage = $event"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HomeView from './views/HomeView.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'

const currentPage = ref('home')
</script>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

#app {
  min-height: 100vh;
}
</style>