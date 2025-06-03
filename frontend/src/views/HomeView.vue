<template>
  <div class="home d-flex align-items-center" style="min-height: 80vh;">
    <div class="container text-center">
      <h1 class="mb-4">Bienvenue sur l'application Smart City</h1>
      <p class="lead">
        Visualisez et analysez les données environnementales de votre ville.
      </p>
      <div class="mt-4">
        <router-link to="/login" class="btn btn-primary me-2">Se connecter</router-link>
        <router-link to="/register" class="btn btn-outline-primary">S'inscrire</router-link>
      </div>
    </div>
  </div>
</template>



<style scoped>
.home {
  padding-top: 60px;
}
</style>
