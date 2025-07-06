<template>
  <div class="container">
    <h2 class="mb-4">Alertes météo</h2>

    <div class="mb-3">
      <select v-model="selectedCityName" class="form-select w-auto">
        <option v-for="c in cities" :key="c.name" :value="c.name">{{ c.name }}</option>
      </select>
    </div>

    <div v-if="alerts.length" class="list-group">
      <div v-for="(alert, i) in alerts" :key="i"
           class="list-group-item"
           :class="levelClass(alert.level)">
        <div class="d-flex justify-content-between">
          <strong><i :class="icon(alert.type)" class="me-2"></i>{{ alert.type }}</strong>
          <small>{{ alert.time }}</small>
        </div>
        <p class="mb-0">{{ alert.message }}</p>
      </div>
    </div>

    <div v-else class="alert alert-info mt-3">Aucune alerte détectée.</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import apiClient from '@/api'

const cities = [
  { name: 'Lyon', lat: 45.76, lon: 4.84 },
  { name: 'Paris', lat: 48.8566, lon: 2.3522 },
  { name: 'Marseille', lat: 43.2965, lon: 5.3698 }
]

const selectedCityName = ref('Lyon')
const selectedCity = computed(() => cities.find(c => c.name === selectedCityName.value))
const alerts = ref([])
const error = ref(null)

async function fetchAlerts () {
  error.value = null
  try {
    const { lat, lon } = selectedCity.value
    const { data } = await apiClient.get('api/weather/', {
      params: { lat, lon }
    })

    const now = new Date().toLocaleString()
    const generated = []

    const temp = data.current_weather?.temperature
    const humid = data.hourly?.relative_humidity_2m?.[0]
    const precip = data.daily?.precipitation_sum?.[0]

    if (temp >= 35) {
      generated.push({
        type: 'Canicule',
        message: `Température très élevée détectée : ${temp}°C`,
        level: 'élevé',
        time: now
      })
    }

    if (humid >= 90) {
      generated.push({
        type: 'Humidité extrême',
        message: `Humidité inhabituelle détectée : ${humid}%`,
        level: 'modéré',
        time: now
      })
    }

    if (precip >= 30) {
      generated.push({
        type: 'Pluie abondante',
        message: `Quantité élevée de pluie prévue aujourd’hui : ${precip} mm`,
        level: 'modéré',
        time: now
      })
    }

    alerts.value = generated

  } catch (err) {
    error.value = "Impossible de récupérer les données météo."
    console.error(err)
  }
}

watch(selectedCityName, fetchAlerts, { immediate: true })

const icon = (type) => {
  if (type.includes('Canicule')) return 'bi bi-thermometer-sun'
  if (type.includes('Humidité')) return 'bi bi-droplet'
  if (type.includes('Pluie')) return 'bi bi-cloud-drizzle'
  return 'bi bi-exclamation-triangle'
}

const levelClass = (level) => {
  if (level === 'élevé') return 'list-group-item-danger'
  if (level === 'modéré') return 'list-group-item-warning'
  return 'list-group-item-secondary'
}
</script>

<style scoped>
.bi {
  font-size: 1.2rem;
}
</style>
