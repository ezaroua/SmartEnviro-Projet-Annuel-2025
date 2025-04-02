<template>
  <div class="register-container">
    <div class="card">
      <h2 class="card-header">Inscription</h2>
      <div class="card-body">
        <div v-if="registrationSuccess" class="success-message">
          <div class="alert alert-success mb-4">
            Inscription réussie! Vous pouvez maintenant vous connecter.
          </div>
          <div class="d-grid">
            <button class="btn btn-primary" @click="$emit('navigate', 'login')">
              Aller à la page de connexion
            </button>
          </div>
        </div>
        
        <form v-else @submit.prevent="handleRegister">
          <div class="alert alert-danger" v-if="errorMessage">{{ errorMessage }}</div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="username">Nom d'utilisateur*</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="userData.username"
                required
                placeholder="Choisissez un nom d'utilisateur"
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="email">Email*</label>
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="userData.email"
                required
                placeholder="Entrez votre email"
              />
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="first_name">Prénom</label>
              <input
                type="text"
                class="form-control"
                id="first_name"
                v-model="userData.first_name"
                placeholder="Votre prénom"
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="last_name">Nom</label>
              <input
                type="text"
                class="form-control"
                id="last_name"
                v-model="userData.last_name"
                placeholder="Votre nom"
              />
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="password">Mot de passe*</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="userData.password"
                required
                placeholder="Choisissez un mot de passe"
              />
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="password2">Confirmer le mot de passe*</label>
              <input
                type="password"
                class="form-control"
                id="password2"
                v-model="userData.password2"
                required
                placeholder="Confirmez le mot de passe"
              />
            </div>
          </div>
          
          <div class="mb-3">
            <label for="phone_number">Téléphone (optionnel)</label>
            <input
              type="tel"
              class="form-control"
              id="phone_number"
              v-model="userData.phone_number"
              placeholder="Votre numéro de téléphone"
            />
          </div>
          
          <div class="mb-3">
            <label for="address">Adresse (optionnel)</label>
            <textarea
              class="form-control"
              id="address"
              v-model="userData.address"
              rows="2"
              placeholder="Votre adresse"
            ></textarea>
          </div>
          
          <div class="mb-3">
            <label for="preferred_district">Quartier préféré (optionnel)</label>
            <input
              type="text"
              class="form-control"
              id="preferred_district"
              v-model="userData.preferred_district"
              placeholder="Votre quartier d'intérêt"
            />
          </div>
          
          <div class="form-check mb-3">
            <input
              type="checkbox"
              class="form-check-input"
              id="receive_alerts"
              v-model="userData.receive_alerts"
            />
            <label class="form-check-label" for="receive_alerts">
              Recevoir des alertes
            </label>
          </div>
          
          <div class="mb-3">
            <button class="btn btn-primary w-100" type="submit" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              S'inscrire
            </button>
          </div>
          
          <div class="text-center">
            Vous avez déjà un compte ?
            <a href="#" @click.prevent="$emit('navigate', 'login')">Connectez-vous ici</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'


const emit = defineEmits(['navigate'])

const userData = ref({
  username: '',
  email: '',
  password: '',
  password2: '',
  first_name: '',
  last_name: '',
  phone_number: '',
  address: '',
  preferred_district: '',
  receive_alerts: true
})
const errorMessage = ref('')
const isLoading = ref(false)
const registrationSuccess = ref(false)

const handleRegister = async () => {

  if (userData.value.password !== userData.value.password2) {
    errorMessage.value = 'Les mots de passe ne correspondent pas'
    return
  }
  
  if (userData.value.password.length < 8) {
    errorMessage.value = 'Le mot de passe doit contenir au moins 8 caractères'
    return
  }
  

  if (!userData.value.email || !userData.value.username) {
    errorMessage.value = "L'email et le nom d'utilisateur sont obligatoires"
    return
  }
  
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    // Envoi des données d'inscription à l'API
    const response = await axios.post('http://localhost:8000/api/register/', {
      username: userData.value.username,
      email: userData.value.email,
      password: userData.value.password,
      password2: userData.value.password2,
      first_name: userData.value.first_name,
      last_name: userData.value.last_name,
      phone_number: userData.value.phone_number,
      address: userData.value.address,
      preferred_district: userData.value.preferred_district,
      receive_alerts: userData.value.receive_alerts
    })
    
    // Si l'inscription est réussie
    if (response.data && response.data.success) {
      registrationSuccess.value = true
      
      // Réinitialiser le formulaire
      userData.value = {
        username: '',
        email: '',
        password: '',
        password2: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        address: '',
        preferred_district: '',
        receive_alerts: true
      }
    } else {
      errorMessage.value = 'Une erreur est survenue lors de l\'inscription'
    }
    
  } catch (error) {

    if (error.response && error.response.data) {
    
      const errors = error.response.data.errors || error.response.data
      
      if (typeof errors === 'object') {
      
        errorMessage.value = Object.entries(errors)
          .map(([field, message]) => {
            if (Array.isArray(message)) {
              return `${field}: ${message.join(', ')}`
            } else {
              return `${field}: ${message}`
            }
          })
          .join('\n')
      } else {
        // Si les erreurs sont une chaîne de caractères
        errorMessage.value = String(errors)
      }
    } else if (error.request) {
      
      errorMessage.value = 'Impossible de contacter le serveur. Veuillez vérifier votre connexion internet.'
    } else {
   
      errorMessage.value = 'Une erreur s\'est produite. Veuillez réessayer.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.card {
  width: 100%;
  max-width: 600px;
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
</style>