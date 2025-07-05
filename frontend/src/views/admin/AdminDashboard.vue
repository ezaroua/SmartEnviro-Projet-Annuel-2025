<template>
  <div class="container py-4">
    <h2 class="mb-4">📊 Tableau de bord administrateur</h2>

    <!-- Statistiques -->
    <div class="row g-3 mb-4">
      <div class="col-md-4" v-for="stat in statsList" :key="stat.label">
        <div class="card text-center shadow">
          <div class="card-body">
            <h5 class="card-title">{{ stat.label }}</h5>
            <p class="display-6 fw-bold text-primary">{{ stat.value }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Graphique inscriptions -->
    <div class="card mb-4">
      <div class="card-header fw-bold">📈 Inscriptions (7 derniers jours)</div>
      <div class="card-body" style="height: 400px;">
        <Line
          v-if="chartData.datasets.length"
          :data="chartData"
          :options="chartOptions"
        />
        <p v-else class="text-muted">Chargement des données...</p>
      </div>
    </div>

    <!-- Derniers utilisateurs -->
    <div class="card">
      <div class="card-header fw-bold">👥 Derniers utilisateurs inscrits</div>
      <div class="table-responsive">
        <table class="table table-striped align-middle text-center mb-0">
          <thead>
            <tr>
              <th>#</th>
              <th>Nom d'utilisateur</th>
              <th>Email</th>
              <th>Date d'inscription</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, idx) in lastUsers" :key="user.id">
              <td>{{ idx + 1 }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ formatDate(user.date_joined) }}</td>
            </tr>
            <tr v-if="lastUsers.length === 0">
              <td colspan="4" class="text-muted">Aucun utilisateur récent</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js'

// Registration
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

// States
const stats = ref({})
const lastUsers = ref([])
const weeklyRegistrations = ref([0,0,0,0,0,0,0])
const error = ref('')

// Fetch
const fetchStats = async () => {
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://localhost:8000/api/admin/dashboard-stats/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    stats.value = data || {}
    lastUsers.value = data.last_users || []
    weeklyRegistrations.value = Array.isArray(data.weekly_registrations) ? data.weekly_registrations : [0,0,0,0,0,0,0]
  } catch (e) {
    error.value = "Erreur lors du chargement des statistiques."
    console.error(e)
  }
}

onMounted(fetchStats)

// Stats display
const statsList = computed(() => [
  { label: "Total utilisateurs", value: stats.value.total_users ?? '--' },
  { label: "Administrateurs", value: stats.value.admins ?? '--' },
  { label: "Citoyens", value: stats.value.citizens ?? '--' },
  { label: "Actifs", value: stats.value.active_users ?? '--' },
  { label: "Inactifs", value: stats.value.inactive_users ?? '--' }
])

// Chart data
const chartData = computed(() => ({
  labels: ["Jour -6", "Jour -5", "Jour -4", "Jour -3", "Jour -2", "Jour -1", "Aujourd'hui"],
  datasets: [{
    label: "Inscriptions",
    data: weeklyRegistrations.value,
    borderColor: "#0d6efd",
    backgroundColor: "rgba(13, 110, 253, 0.2)",
    tension: 0.3,
    fill: true,
    pointRadius: 5,
    pointBackgroundColor: "#0d6efd"
  }]
}))

// Chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: true, position: 'top' },
    tooltip: { enabled: true }
  },
  scales: {
    y: { beginAtZero: true, precision: 0 },
    x: { ticks: { autoSkip: false } }
  }
}

// Format date
function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}
</script>

<style scoped>
.table th,
.table td {
  vertical-align: middle;
}

.card-header {
  font-weight: 600;
}

.display-6 {
  font-size: 2rem;
}

.card {
  border-radius: 0.5rem;
}

.shadow {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
</style>
