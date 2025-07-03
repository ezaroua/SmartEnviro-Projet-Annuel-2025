<template>
  <div class="container py-4">
    <h2 class="mb-4">👥 Gestion des utilisateurs</h2>

    <!-- Filtre rôle -->
    <div class="mb-3 d-flex align-items-center gap-2">
      <label>Filtrer par rôle:</label>
      <select v-model="roleFilter" class="form-select w-auto">
        <option value="">Tous</option>
        <option value="admin">Admin</option>
        <option value="citizen">Citoyen</option>
      </select>
      <button class="btn btn-secondary btn-sm" @click="fetchUsers">
        Rafraîchir
      </button>
    </div>

    <!-- Table utilisateurs -->
    <div class="table-responsive">
      <table class="table table-bordered align-middle text-center">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Nom d'utilisateur</th>
            <th>Email</th>
            <th>Rôle</th>
            <th>Actif</th>
            <th>Date d'inscription</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, idx) in filteredUsers" :key="user.id">
            <td>{{ idx + 1 }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
              <span :class="user.is_active ? 'text-success' : 'text-danger'">
                {{ user.is_active ? 'Oui' : 'Non' }}
              </span>
            </td>
            <td>{{ formatDate(user.date_joined) }}</td>
            <td>
              <button
                class="btn btn-sm"
                :class="user.is_active ? 'btn-warning' : 'btn-success'"
                @click="toggleActive(user)"
              >
                {{ user.is_active ? 'Désactiver' : 'Activer' }}
              </button>
              <button
                class="btn btn-danger btn-sm ms-1"
                @click="deleteUser(user)"
              >
                Supprimer
              </button>
            </td>
          </tr>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="7" class="text-muted">Aucun utilisateur trouvé</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])
const error = ref('')
const roleFilter = ref('')

/* Charger utilisateurs */
async function fetchUsers() {
  error.value = ''
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://localhost:8000/api/users/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    users.value = data
  } catch (e) {
    error.value = "Erreur lors du chargement des utilisateurs."
    console.error(e)
  }
}

/* Activer / Désactiver */
async function toggleActive(user) {
  try {
    const token = localStorage.getItem('token')
    await axios.patch(`http://localhost:8000/api/users/${user.id}/toggle_active/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchUsers()
  } catch (e) {
    error.value = "Erreur lors de la mise à jour de l'utilisateur."
    console.error(e)
  }
}

/* Supprimer utilisateur */
async function deleteUser(user) {
  if (!confirm(`Supprimer ${user.username} ?`)) return
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://localhost:8000/api/users/${user.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    fetchUsers()
  } catch (e) {
    error.value = "Erreur lors de la suppression de l'utilisateur."
    console.error(e)
  }
}

/* Format date */
function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

/* Filtrage selon rôle */
const filteredUsers = computed(() => {
  if (!roleFilter.value) return users.value
  return users.value.filter(user => user.role === roleFilter.value)
})

onMounted(fetchUsers)
</script>

<style scoped>
.table th, .table td {
  vertical-align: middle;
}
</style>
