<template>
  <div class="profile-container">
    <div class="container py-4">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h2 class="mb-0">Mon profil</h2>
            </div>
            <div class="card-body">
              <div v-if="errorMessage" class="alert alert-danger mb-3">
                {{ errorMessage }}
              </div>
              <div v-if="successMessage" class="alert alert-success mb-3">
                {{ successMessage }}
              </div>
              
              <form @submit.prevent="updateProfile">
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="username" class="form-label">Nom d'utilisateur</label>
                    <input type="text" class="form-control" id="username" value="utilisateur_demo" disabled />
                  </div>
                  <div class="col-md-6">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" value="demo@example.com" disabled />
                  </div>
                </div>
                
                <div class="row mb-3">
                  <div class="col-md-6">
                    <label for="firstName" class="form-label">Prénom</label>
                    <input type="text" class="form-control" id="firstName" v-model="profile.firstName" />
                  </div>
                  <div class="col-md-6">
                    <label for="lastName" class="form-label">Nom</label>
                    <input type="text" class="form-control" id="lastName" v-model="profile.lastName" />
                  </div>
                </div>
                
                <div class="mb-3">
                  <label for="phoneNumber" class="form-label">Téléphone</label>
                  <input type="tel" class="form-control" id="phoneNumber" v-model="profile.phoneNumber" />
                </div>
                
                <div class="mb-3">
                  <label for="address" class="form-label">Adresse</label>
                  <textarea class="form-control" id="address" rows="2" v-model="profile.address"></textarea>
                </div>
                
                <div class="mb-3">
                  <label for="district" class="form-label">Quartier préféré</label>
                  <input type="text" class="form-control" id="district" v-model="profile.district" />
                </div>
                
                <div class="form-check mb-3">
                  <input class="form-check-input" type="checkbox" id="receiveAlerts" v-model="profile.receiveAlerts" />
                  <label class="form-check-label" for="receiveAlerts">
                    Recevoir des alertes
                  </label>
                </div>
                
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary">Mettre à jour le profil</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const profile = ref({
  firstName: 'Utilisateur',
  lastName: 'Démo',
  phoneNumber: '0123456789',
  address: '123 Rue Exemple, 75000 Paris',
  district: 'Centre-Ville',
  receiveAlerts: true
})

const errorMessage = ref('')
const successMessage = ref('')

const updateProfile = () => {
  
  successMessage.value = 'Profil mis à jour avec succès'
  
 
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}
</script>