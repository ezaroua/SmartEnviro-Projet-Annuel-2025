<template>
  <nav class="navbar navbar-light bg-light shadow-sm">
    <div class="container">
      <router-link class="navbar-brand" to="/">Smart City</router-link>
      <div>
        <router-link class="btn btn-outline-primary me-2" to="/login">Connexion</router-link>
        <router-link class="btn btn-primary" to="/register">Inscription</router-link>
      </div>
    </div>
  </nav>
  <router-view/>
</template>
