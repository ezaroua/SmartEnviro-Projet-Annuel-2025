<template>
  <div class="container-fluid">
    <!-- Sélecteur de ville -->
    <div class="mb-3">
      <label class="form-label">Sélectionnez une ville :</label>
      <select v-model="selectedCityName" @change="onCityChange" class="form-select w-auto mb-2">
        <option v-for="c in cities" :key="c.name" :value="c.name">
          {{ c.name }}
        </option>
      </select>
      
      <!-- Boutons de test -->
      <div class="btn-group mb-2" role="group">
        <button v-for="city in cities" :key="city.name" 
                @click="selectCity(city.name)"
                :class="['btn', 'btn-sm', selectedCityName === city.name ? 'btn-primary' : 'btn-outline-primary']">
          {{ city.name }}
        </button>
      </div>
      
      <div>
        <small class="text-muted">Ville sélectionnée: <strong>{{ selectedCityName }}</strong></small>
      </div>
    </div>

    <!-- Indicateurs -->
    <div class="row g-3 mb-4">
      <div class="col-12 mb-2">
        <h5 class="text-primary">Météo pour {{ selectedCityName }}</h5>
        <small class="text-muted">Coordonnées: {{ selectedCity.lat }}, {{ selectedCity.lon }}</small>
      </div>
      <Indicator icon="bi-thermometer-half" color="primary"
                 label="Température" :value="temperature + ' °C'"/>
      <Indicator icon="bi-droplet" color="info"
                 label="Humidité" :value="humidity + ' %'"/>
      <Indicator icon="bi-wind" color="success"
                 label="Vent" :value="wind + ' km/h'"/>
      <Indicator icon="bi-cloud-drizzle" color="secondary"
                 label="Pluie aujourd'hui" :value="precipToday + ' mm'"/>
      <Indicator icon="bi-cloud-rain" color="warning"
           label="Précipitations demain" :value="precipTomorrow + ' %'"/>

    </div>

    <!-- Graph précipitations 7 jours -->
    <div class="card mb-4">
      <div class="card-header">
        <h6 class="mb-0">Précipitations prévues - {{ selectedCityName }} (7 jours)</h6>
      </div>
      <div class="card-body">
        <div v-if="isLoading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Chargement...</span>
          </div>
        </div>
        <LineChart v-else-if="hasValidChartData"
                   :data="rainChart"
                   :options="chartOptions"
                   height="300"/>
        <p v-else class="text-muted mb-0">Aucune donnée de précipitation disponible pour {{ selectedCityName }}.</p>
      </div>
    </div>

    <!-- Carte -->
    <div class="card">
      <div class="card-header">
        <h6 class="mb-0">Carte de France</h6>
      </div>
      <div class="card-body p-0">
        <div id="map" style="height:400px"></div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import axios from 'axios'
import L from 'leaflet'
import Indicator from '@/components/Indicator.vue'

import { Line as LineChart } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js'
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

const cities = [
  { name:'Paris',      lat:48.8566, lon:2.3522 },
  { name:'Lyon',       lat:45.7578, lon:4.832 },
  { name:'Marseille',  lat:43.2965, lon:5.3698 },
  { name:'Bordeaux',   lat:44.8378, lon:-0.5792 },
  { name:'Lille',      lat:50.6292, lon:3.0573 }
]

const selectedCityName = ref(cities[0].name)
const selectedCity = computed(() => cities.find(c => c.name === selectedCityName.value))

const weatherData = ref(null)
const isLoading = ref(false)
const error = ref(null)

// Fonction pour sélectionner une ville
function selectCity(cityName) {
  console.log(`Sélection manuelle de: ${cityName}`)
  selectedCityName.value = cityName
}

// Fonction pour gérer le changement de ville via le select
function onCityChange() {
  console.log(` Changement via select: ${selectedCityName.value}`)
}

// Fonction pour récupérer les données météo
async function fetchWeatherData() {
  if (!selectedCity.value) return
  
  error.value = null
  isLoading.value = true
  
  try {
    const city = selectedCity.value
    console.log(` Récupération météo pour ${city.name} (lat: ${city.lat}, lon: ${city.lon})`)
    
    const response = await axios.get('http://localhost:8000/api/weather/', {
      params: { 
        lat: city.lat, 
        lon: city.lon 
      }
    })
    
    console.log(` Données reçues pour ${city.name}:`, response.data)
    weatherData.value = response.data
    
  } catch (err) {
    console.error(` Erreur API pour ${selectedCity.value.name}:`, err)
    error.value = `Impossible de récupérer les données météo pour ${selectedCity.value.name}`
    weatherData.value = null
  } finally {
    isLoading.value = false
  }
}

// Watcher pour détecter le changement de ville
watch(selectedCityName, async (newCityName, oldCityName) => {
  console.log(` Changement de ville: ${oldCityName} → ${newCityName}`)
  await fetchWeatherData()
  
  // Centrer la carte sur la nouvelle ville
  if (map && selectedCity.value) {
    console.log(` Centrage carte sur ${selectedCity.value.name}`)
    map.setView([selectedCity.value.lat, selectedCity.value.lon], 9)
  }
})

let map
let markers = []

onMounted(async () => {
  await nextTick()
  
  // Chargement initial des données
  console.log('Chargement initial des données')
  await fetchWeatherData()
  
  // Initialisation de la carte
  map = L.map('map').setView([46.6, 1.8], 6)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map)

  // Ajouter les marqueurs pour chaque ville
  cities.forEach(city => {
    const marker = L.marker([city.lat, city.lon])
      .addTo(map)
      .bindPopup(`<strong>${city.name}</strong><br>Cliquez pour voir la météo`)
      
    marker.on('click', () => {
      console.log(`Clic sur marqueur: ${city.name}`)
      console.log(` Avant changement: ${selectedCityName.value}`)
      selectedCityName.value = city.name
      console.log(`Après changement: ${selectedCityName.value}`)
    })
    
    markers.push(marker)
  })
})

// Computed pour extraire les données météo
const temperature = computed(() => {
  const temp = weatherData.value?.current_weather?.temperature
  return temp !== undefined ? Math.round(temp) : '--'
})

const humidity = computed(() => {
  const humid = weatherData.value?.hourly?.relative_humidity_2m?.[0]
  return humid !== undefined ? Math.round(humid) : '--'
})

const wind = computed(() => {
  const windSpeed = weatherData.value?.current_weather?.windspeed
  return windSpeed !== undefined ? Math.round(windSpeed) : '--'
})

const precipToday = computed(() => {
  const precip = weatherData.value?.daily?.precipitation_sum?.[0]
  return precip !== undefined ? precip.toFixed(1) : '--'
})

// Vérifier si les données du graphique sont valides
const hasValidChartData = computed(() => {
  return weatherData.value?.daily?.precipitation_sum && 
         weatherData.value?.daily?.time &&
         weatherData.value.daily.precipitation_sum.length > 0 &&
         weatherData.value.daily.time.length > 0
})

// Graphique des précipitations sur 7 jours
const rainChart = computed(() => {
  if (!hasValidChartData.value) {
    console.log(' Pas de données de précipitation disponibles')
    return {
      labels: [],
      datasets: []
    }
  }
  
  const precipData = weatherData.value.daily.precipitation_sum
  const timeData = weatherData.value.daily.time
  
  console.log('Données précipitations:', precipData)
  console.log('Données dates:', timeData)
  
  const labels = timeData.map(date => {
    const d = new Date(date)
    return d.toLocaleDateString('fr-FR', { 
      weekday: 'short', 
      day: '2-digit',
      month: '2-digit'
    })
  })
  
  return {
    labels: labels,
    datasets: [{
      label: `Précipitations ${selectedCityName.value} (mm)`,
      data: precipData,
      borderColor: '#0dcaf0',
      backgroundColor: 'rgba(13, 202, 240, 0.1)',
      tension: 0.3,
      fill: true,
      pointBackgroundColor: '#0dcaf0',
      pointBorderColor: '#ffffff',
      pointBorderWidth: 2,
      pointRadius: 4
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: ${context.parsed.y} mm`
        }
      }
    }
  },
  scales: {
    x: {
      display: true,
      title: {
        display: true,
        text: 'Jours'
      }
    },
    y: {
      display: true,
      beginAtZero: true,
      title: {
        display: true,
        text: 'Précipitations (mm)'
      }
    }
  },
  elements: {
    line: {
      tension: 0.3
    }
  }
}
</script>

<style scoped>
.card-header {
  font-weight: bold;
  background-color: #f8f9fa;
}

.spinner-border {
  width: 2rem;
  height: 2rem;
}

.text-primary {
  color: #0d6efd !important;
}

.text-muted {
  font-size: 0.875rem;
}
</style>