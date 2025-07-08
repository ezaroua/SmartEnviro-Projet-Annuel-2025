<template>
  <div class="container py-4" v-if="loaded">
    <h3 class="mb-4">Mon profil</h3>

    <div v-if="success" class="alert alert-success">{{ success }}</div>
    <div v-if="error"   class="alert alert-danger">{{ error }}</div>

    <form @submit.prevent="updateProfile" class="row g-3">
      <div class="col-md-6">
        <label class="form-label">Prénom</label>
        <input v-model="profile.first_name" class="form-control"/>
      </div>
      <div class="col-md-6">
        <label class="form-label">Nom</label>
        <input v-model="profile.last_name" class="form-control"/>
      </div>

      <div class="col-md-6">
        <label class="form-label">Email</label>
        <input v-model="profile.email" type="email" class="form-control"/>
      </div>
      <div class="col-md-6">
        <label class="form-label">Téléphone</label>
        <input v-model="profile.phone_number" class="form-control"/>
      </div>

      <div class="col-12">
        <label class="form-label">Adresse</label>
        <input v-model="profile.address" class="form-control"/>
      </div>

      <div class="col-md-6">
        <label class="form-label">Quartier préféré</label>
        <input v-model="profile.preferred_district" class="form-control"/>
      </div>

      <div class="col-md-6 form-check align-self-end">
        <input id="alerts" type="checkbox" v-model="profile.receive_alerts"
               class="form-check-input"/>
        <label for="alerts" class="form-check-label">Recevoir les alertes</label>
      </div>

      <div class="col-12 mt-3">
        <button class="btn btn-primary" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"/>
          Enregistrer
        </button>
      </div>
    </form>

    <hr class="my-5"/>

    <h4>Changer mon mot de passe</h4>

    <form @submit.prevent="changePassword" class="row g-3 col-md-6">
      <div>
        <label class="form-label">Ancien mot de passe</label>
        <input type="password" v-model="pwd.old" class="form-control" required/>
      </div>
      <div>
        <label class="form-label">Nouveau mot de passe</label>
        <input type="password" v-model="pwd.new1" class="form-control" required/>
      </div>
      <div>
        <label class="form-label">Confirmer le nouveau</label>
        <input type="password" v-model="pwd.new2" class="form-control" required/>
      </div>

      <div>
        <button class="btn btn-outline-primary" :disabled="pwdLoading">
          <span v-if="pwdLoading" class="spinner-border spinner-border-sm me-2"/>
          Mettre à jour le mot de passe
        </button>
      </div>

      <div v-if="pwdSuccess" class="alert alert-success mt-2">{{ pwdSuccess }}</div>
      <div v-if="pwdError"   class="alert alert-danger  mt-2">{{ pwdError }}</div>
    </form>
  </div>

  <div v-else class="text-center py-5">
    <span class="spinner-border"/>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const profile = ref({})
const loaded  = ref(false)
const loading = ref(false)
const error   = ref('')
const success = ref('')
const pwd         = ref({ old:'', new1:'', new2:'' })
const pwdLoading  = ref(false)
const pwdSuccess  = ref('')
const pwdError    = ref('')

async function changePassword () {
  pwdSuccess.value = ''; pwdError.value = ''; pwdLoading.value = true

  try {
    await axios.patch('http://localhost:8000/api/change-password/', {
      old_password:      pwd.value.old,
      new_password:      pwd.value.new1,
      new_password_conf: pwd.value.new2
    }, { headers: authHeader() })

    pwdSuccess.value = 'Mot de passe mis à jour – vous devrez vous reconnecter.'
    // vider les champs
    pwd.value = { old:'', new1:'', new2:'' }
    // option : déconnexion après 3 s
    setTimeout(() => {
      localStorage.clear()
      location.href = '/login'
    }, 3000)

  } catch (e) {
    pwdError.value = e.response?.data?.old_password?.[0] ||
                     e.response?.data?.new_password?.[0]  ||
                     e.response?.data?.detail              ||
                     'Erreur'
  } finally {
    pwdLoading.value = false
  }
}

function authHeader () {
  return { Authorization:`Bearer ${localStorage.getItem('token')}` }
}

async function getProfile () {
  try {
    const { data } = await axios.get('http://localhost:8000/api/me/', {
      headers: authHeader()
    })
    profile.value = data
  } catch (e) {
    error.value = 'Impossible de charger le profil'
  } finally {
    loaded.value = true
  }
}

async function updateProfile () {
  try {
    error.value = ''; success.value = ''; loading.value = true
    const { data } = await axios.patch('http://localhost:8000/api/me/', profile.value, {
      headers: authHeader()
    })
    profile.value = data
    success.value = 'Profil mis à jour avec succès'
  } catch {
    error.value = 'Erreur lors de la mise à jour'
  } finally { loading.value = false }
}

onMounted(getProfile)
</script>
