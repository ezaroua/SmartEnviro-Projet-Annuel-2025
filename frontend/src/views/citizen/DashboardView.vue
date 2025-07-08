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
                 label="Probabilité de pluie demain" :value="predictedRainChance"/> <!-- Renommé pour la probabilité -->

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
import apiClient from '@/api'
import L from 'leaflet'
import Indicator from '@/components/Indicator.vue'

import { 
  Line as LineChart 
} from 'vue-chartjs'
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Tooltip, 
  Legend,
  Filler 
} from 'chart.js'

ChartJS.register(
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Tooltip, 
  Legend,
  Filler 
)

const cities = [
  { name:'Paris',       lat:48.8566, lon:2.3522 },
  { name:'Lyon',        lat:45.7578, lon:4.832 },
  { name:'Marseille',   lat:43.2965, lon:5.3698 },
  { name:'Bordeaux',    lat:44.8378, lon:-0.5792 },
  { name:'Lille',       lat:50.6292, lon:3.0573 }
]

const selectedCityName = ref(cities[0].name)
const selectedCity = computed(() => cities.find(c => c.name === selectedCityName.value))

const weatherData = ref(null) 
const isLoading = ref(false)
const error = ref(null)
const predictedRainChance = ref('--') 

function selectCity(cityName) {
  console.log(`Sélection manuelle de: ${cityName}`)
  selectedCityName.value = cityName
}

function onCityChange() {
  console.log(`Changement via select: ${selectedCityName.value}`)
}

async function fetchWeatherData() {
  if (!selectedCity.value) return

  error.value = null
  isLoading.value = true

  try {
    const city = selectedCity.value
    console.log(` Récupération météo pour ${city.name} (lat: ${city.lat}, lon: ${city.lon})`)
    
    const response = await apiClient.get('api/weather/', {
      params: { 
        lat: city.lat, 
        lon: city.lon 
      }
    })

    console.log(`Données reçues pour ${city.name}:`, response.data)
    weatherData.value = response.data

  } catch (err) {
    console.error(`Erreur API pour ${selectedCity.value.name}:`, err)
    error.value = `Impossible de récupérer les données météo pour ${selectedCity.value.name}`
    weatherData.value = null
  } finally {
    isLoading.value = false
  }
}

watch(selectedCityName, async (newCityName, oldCityName) => {
  console.log(`Changement de ville: ${oldCityName} → ${newCityName}`)
  await fetchWeatherData()
  await fetchPrediction() 
  if (map && selectedCity.value) {
    console.log(`Centrage carte sur ${selectedCity.value.name}`)
    map.setView([selectedCity.value.lat, selectedCity.value.lon], 9)
  }
})

let map
let markers = []

onMounted(async () => {
  await nextTick()

  console.log('Chargement initial des données')
  await fetchWeatherData()
  await fetchPrediction() 

  map = L.map('map').setView([46.6, 1.8], 6)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map)

  cities.forEach(city => {
    const marker = L.marker([city.lat, city.lon])
      .addTo(map)
      .bindPopup(`<strong>${city.name}</strong><br>Cliquez pour voir la météo`)

    marker.on('click', () => {
      console.log(`Clic sur marqueur: ${city.name}`)
      selectedCityName.value = city.name
    })

    markers.push(marker)
  })
})

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

const hasValidChartData = computed(() => {
  return weatherData.value?.daily?.precipitation_sum && 
           weatherData.value?.daily?.time &&
           weatherData.value.daily.precipitation_sum.length > 0 &&
           weatherData.value.daily.time.length > 0
})

async function fetchPrediction() {
  try {
    const response = await axios.get('http://localhost:8000/api/weather/weather-daily/', {
      params: { lat: selectedCity.value.lat, lon: selectedCity.value.lon }
    })
    
    console.log('DEBUG FRONTEND: Objet "response" complet d\'Axios:', response);
    console.log('DEBUG FRONTEND: Type de response.data:', typeof response.data);
    console.log('DEBUG FRONTEND: Contenu de response.data (avant assignation):', response.data);

    const weatherDataForModel = response.data; 

    console.log('DEBUG FRONTEND: Contenu de weatherDataForModel (après assignation):', weatherDataForModel);


    if (!weatherDataForModel.daily || Object.keys(weatherDataForModel.daily).length === 0) { 
      console.error('ERREUR FRONTEND: weatherDataForModel.daily est absent, null ou vide alors qu\'il devrait être là.', weatherDataForModel);
      throw new Error('Les données journalières sont absentes de l\'API pour le modèle IA.')
    }

    function safeGet(arr, index = 0, defaultValue = 0) {
      return Array.isArray(arr) && arr.length > index ? arr[index] : defaultValue
    }

    // Extraction des nouvelles features de date/heure
    const dailyTime = safeGet(weatherDataForModel.daily.time, 0, '');
    let dayOfYear = 0, dayOfWeek = 0, month = 0;
    if (dailyTime) {
      const dateObj = new Date(dailyTime);
      dayOfYear = Math.floor((dateObj - new Date(dateObj.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
      dayOfWeek = dateObj.getUTCDay(); // 0 for Sunday, 6 for Saturday
      month = dateObj.getUTCMonth() + 1; // 1 for January, 12 for December
    }

    const sunriseTime = safeGet(weatherDataForModel.daily.sunrise, 0, '');
    let sunriseSeconds = 0;
    if (sunriseTime) {
        const timeParts = sunriseTime.split('T')[1]?.split(':');
        if (timeParts && timeParts.length >= 2) {
            sunriseSeconds = (parseInt(timeParts[0]) * 3600) + (parseInt(timeParts[1]) * 60);
        }
    }

    const sunsetTime = safeGet(weatherDataForModel.daily.sunset, 0, '');
    let sunsetSeconds = 0;
    if (sunsetTime) {
        const timeParts = sunsetTime.split('T')[1]?.split(':');
        if (timeParts && timeParts.length >= 2) {
            sunsetSeconds = (parseInt(timeParts[0]) * 3600) + (parseInt(timeParts[1]) * 60);
        }
    }


    const preparedData = {
      weathercode: safeGet(weatherDataForModel.daily.weathercode, 0), 
      temperature_2m_max: safeGet(weatherDataForModel.daily.temperature_2m_max, 0), 
      temperature_2m_min: safeGet(weatherDataForModel.daily.temperature_2m_min, 0), 
      apparent_temperature_max: safeGet(weatherDataForModel.daily.apparent_temperature_max, 0), 
      apparent_temperature_min: safeGet(weatherDataForModel.daily.apparent_temperature_min, 0), 
      daylight_duration: safeGet(weatherDataForModel.daily.daylight_duration, 0), 
      sunshine_duration: safeGet(weatherDataForModel.daily.sunshine_duration, 0), 
      uv_index_max: safeGet(weatherDataForModel.daily.uv_index_max, 0), 
      uv_index_clear_sky_max: safeGet(weatherDataForModel.daily.uv_index_clear_sky_max, 0), 
      rain_sum: safeGet(weatherDataForModel.daily.rain_sum, 0), 
      showers_sum: safeGet(weatherDataForModel.daily.showers_sum, 0), 
      snowfall_sum: safeGet(weatherDataForModel.daily.snowfall_sum, 0), 
      precipitation_sum: safeGet(weatherDataForModel.daily.precipitation_sum, 0), 
      precipitation_hours: safeGet(weatherDataForModel.daily.precipitation_hours, 0), 
      windspeed_10m_max: safeGet(weatherDataForModel.daily.windspeed_10m_max, 0), 
      windgusts_10m_max: safeGet(weatherDataForModel.daily.windgusts_10m_max, 0), 
      winddirection_10m_dominant: safeGet(weatherDataForModel.daily.winddirection_10m_dominant, 0), 
      shortwave_radiation_sum: safeGet(weatherDataForModel.daily.shortwave_radiation_sum, 0), 
      et0_fao_evapotranspiration: safeGet(weatherDataForModel.daily.et0_fao_evapotranspiration, 0),
      // Ajout des nouvelles features numériques de date/heure
      day_of_year: dayOfYear,
      day_of_week: dayOfWeek,
      month: month,
      sunrise_seconds: sunriseSeconds,
      sunset_seconds: sunsetSeconds,
    }

    const nullCount = Object.values(preparedData).filter(val => val === null).length
    if (nullCount > 0) {
      console.warn(`Attention: ${nullCount} données nulles détectées dans preparedData. Elles devraient être 0.`, preparedData)
    }
    
    console.log('Données préparées pour la prédiction:', preparedData)

    const predictionResponse = await axios.post('http://127.0.0.1:5000/predict', preparedData)

    console.log('--- DEBUG API PREDICTION ---')
    console.log('Réponse complète:', predictionResponse)
    console.log('Type de predictionResponse.data:', typeof predictionResponse.data)
    console.log('Contenu de predictionResponse.data:', predictionResponse.data)
    console.log('Clés disponibles:', Object.keys(predictionResponse.data || {}))
    console.log('--- FIN DEBUG ---')

    // SIMPLIFICATION ICI : Accès direct à prediction_probability
    if (!predictionResponse.data || typeof predictionResponse.data.prediction_probability === 'undefined') {
      throw new Error('Réponse inattendue de l\'API de prédiction: "prediction_probability" est manquant ou indéfini.')
    }

    let predictionProbability = predictionResponse.data.prediction_probability

    if (typeof predictionProbability === 'number') {
      predictedRainChance.value = `${(predictionProbability * 100).toFixed(1)} %`
    } else {
      predictedRainChance.value = 'N/A'
      console.error('La prédiction reçue n\'est pas un nombre:', predictionProbability)
    }

    console.log("Prédiction IA récupérée (probabilité):", predictedRainChance.value)

  } catch (error) {
    console.error('Erreur détaillée lors de la récupération ou de la prédiction:', error)
    if (error.response) {
      console.error('Statut de réponse:', error.response.status)
      console.error('Données de réponse:', error.response.data)
      error.value = `Erreur API (${error.response.status}): ${error.response.data?.error || 'Erreur inconnue'}`
    } else if (error.request) {
      console.error('Pas de réponse reçue:', error.request)
      error.value = "Impossible de contacter l'API de prédiction."
    } else {
      error.value = `Erreur de prédiction: ${error.message}`
    }
    predictedRainChance.value = '--'
  }
}

const rainChart = computed(() => {
  if (!hasValidChartData.value) {
    console.log('Pas de données de précipitation disponibles')
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
      label: `Précipitations ${selectedCityName.value} (mm)` ,
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
