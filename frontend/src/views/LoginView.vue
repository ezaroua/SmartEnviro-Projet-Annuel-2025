<template>
  <div class="login-container">
    <div class="card">
      <h2 class="card-header">Connexion</h2>
      <div class="card-body">
        <form @submit.prevent="handleLogin">
          <div class="alert alert-danger" v-if="errorMessage">{{ errorMessage }}</div>

          <div class="form-group mb-3">
            <label for="username">Nom d'utilisateur</label>
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="credentials.username"
              required
              placeholder="Entrez votre nom d'utilisateur"
            />
          </div>

          <div class="form-group mb-3">
            <label for="password">Mot de passe</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="credentials.password"
              required
              placeholder="Entrez votre mot de passe"
            />
          </div>

          <div class="form-group mb-3">
            <button class="btn btn-primary w-100" type="submit" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              Connexion
            </button>
          </div>

          <div class="text-center">
            Vous n'avez pas de compte ?
            <router-link to="/register" class="custom-link">Inscrivez-vous ici</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const emit = defineEmits(['navigate'])

const credentials = ref({
  username: '',
  password: ''
})
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  if (!credentials.value.username || !credentials.value.password) {
    errorMessage.value = 'Veuillez remplir tous les champs'
    return
  }

  try {
    isLoading.value = true
    errorMessage.value = ''

    const response = await axios.post('http://localhost:8000/api/token/', {
      username: credentials.value.username,
      password: credentials.value.password
    })

    localStorage.setItem('token',  response.data.access)
    localStorage.setItem('refresh',response.data.refresh)
    localStorage.setItem('role',    String(response.data.role_id))   

    router.push(response.data.role_id === 1 ? '/dashboardAdmin' : '/dashboardCitizen')


  } catch (error) {
    console.error('Erreur login:', error)

    if (error.response) {
      if (error.response.status === 401) {
        errorMessage.value = 'Identifiants incorrects. Veuillez réessayer.'
      } else if (error.response.data.detail) {
        errorMessage.value = error.response.data.detail
      } else {
        errorMessage.value = 'Erreur lors de la connexion. Veuillez réessayer.'
      }
    } else if (error.request) {
      errorMessage.value = 'Impossible de contacter le serveur.'
    } else {
      errorMessage.value = 'Une erreur s\'est produite. Veuillez réessayer.'
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.card {
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
}

.card-body {
  padding: 20px;
}

.custom-link {
  color: #0d6efd; /* bleu Bootstrap */
  text-decoration: underline;
  cursor: pointer;
}

</style>
