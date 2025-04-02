<template>
  <div class="home">
    <div class="container py-5">
      <h1 class="mb-4">Bienvenue sur l'application Smart City</h1>
      <p class="lead">
        Cette plateforme vous permet de visualiser et d'analyser les données environnementales de votre ville.
      </p>
      <div class="mt-4">
        <button class="btn btn-primary me-2" @click="$emit('navigate', 'login')">Se connecter</button>
        <button class="btn btn-outline-primary" @click="$emit('navigate', 'register')">S'inscrire</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Émetteurs d'événements pour la navigation
defineEmits(['navigate'])
</script>

<style scoped>
.home {
  min-height: 80vh;
  display: flex;
  align-items: center;
}
</style>