<template>
  <div class="admin-dashboard">
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Administration</h1>
        <span class="badge bg-success">Mode administrateur</span>
      </div>
      
      <div class="row">
        <div class="col-md-6 mb-4">
          <div class="card h-100">
            <div class="card-header">
              Gestion des utilisateurs
            </div>
            <div class="card-body">
              <h5 class="card-title">Utilisateurs enregistrés</h5>
              <p class="card-text">Total: {{ userCount }} utilisateurs</p>
              
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Nom d'utilisateur</th>
                    <th>Rôle</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>
                      <span :class="user.role === 'admin' ? 'text-danger' : 'text-success'">
                        {{ user.role }}
                      </span>
                    </td>
                    <td>
                      <button class="btn btn-sm btn-outline-primary me-1">Éditer</button>
                      <button class="btn btn-sm btn-outline-danger">Supprimer</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        <div class="col-md-6 mb-4">
          <div class="card h-100">
            <div class="card-header">
              Configuration du système
            </div>
            <div class="card-body">
              <h5 class="card-title">Paramètres globaux</h5>
              
              <form>
                <div class="mb-3">
                  <label for="alertThreshold" class="form-label">Seuil d'alerte (pollution)</label>
                  <input type="number" class="form-control" id="alertThreshold" v-model="settings.alertThreshold" />
                </div>
                
                <div class="mb-3">
                  <label for="updateFrequency" class="form-label">Fréquence de mise à jour (minutes)</label>
                  <input type="number" class="form-control" id="updateFrequency" v-model="settings.updateFrequency" />
                </div>
                
                <div class="form-check mb-3">
                  <input class="form-check-input" type="checkbox" id="enableNotifications" v-model="settings.enableNotifications" />
                  <label class="form-check-label" for="enableNotifications">
                    Activer les notifications système
                  </label>
                </div>
                
                <div class="d-grid">
                  <button type="button" class="btn btn-primary" @click="saveSettings">
                    Enregistrer les paramètres
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              Journal d'activité
            </div>
            <div class="card-body">
              <h5 class="card-title">Dernières actions</h5>
              
              <div class="list-group">
                <div class="list-group-item list-group-item-action" v-for="(log, index) in activityLogs" :key="index">
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ log.action }}</h6>
                    <small>{{ log.time }}</small>
                  </div>
                  <p class="mb-1">{{ log.details }}</p>
                  <small>Utilisateur: {{ log.user }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const userCount = ref(3)
const users = ref([
  { id: 1, username: 'admin', role: 'admin' },
  { id: 2, username: 'utilisateur1', role: 'citizen' },
  { id: 3, username: 'utilisateur2', role: 'citizen' }
])

const settings = ref({
  alertThreshold: 75,
  updateFrequency: 15,
  enableNotifications: true
})

const activityLogs = ref([
  { 
    action: 'Connexion au système',
    details: 'Connexion réussie',
    user: 'admin',
    time: '2023-11-17 14:25'
  },
  { 
    action: 'Mise à jour des paramètres',
    details: 'Seuil d\'alerte modifié: 80 -> 75',
    user: 'admin',
    time: '2023-11-17 14:10'
  },
  { 
    action: 'Nouvel utilisateur',
    details: 'Création du compte utilisateur2',
    user: 'système',
    time: '2023-11-16 09:45'
  }
])

const saveSettings = () => {
  alert('Paramètres enregistrés avec succès!')
}
</script>

<style scoped>
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.card-header {
  background-color: #f8f9fa;
  font-weight: 500;
}
</style>