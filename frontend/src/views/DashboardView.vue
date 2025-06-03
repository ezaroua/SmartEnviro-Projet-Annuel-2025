<template>
  <div class="container-fluid">

    <!-- Sélecteur de ville -->
    <div class="mb-3">
      <select v-model="selectedCityName" class="form-select w-auto">
        <option v-for="c in cities" :key="c.name" :value="c.name">
          {{ c.name }}
        </option>
      </select>
    </div>

    <!-- Indicateurs ------------------------------------------------>
    <div class="row g-3 mb-4">
      <Indicator icon="bi-thermometer-half" color="primary"
                 label="Température" :value="temperature + ' °C'"/>
      <Indicator icon="bi-droplet" color="info"
                 label="Humidité" :value="humidity + ' %'"/>
      <Indicator icon="bi-cloud" color="warning"
                 label="Vent" :value="wind + ' km/h'"/>
      <Indicator icon="bi-cloud-drizzle" color="secondary"
                 label="Pluie aujourd’hui" :value="precipToday + ' mm'"/>
    </div>

    <!-- Graph précipitations 7 jours ------------------------------->
    <div class="card mb-4">
      <div class="card-header">Précipitations prévues (7 jours)</div>
      <div class="card-body">
        <LineChart v-if="rainChart.datasets.length"
                   :chart-data="rainChart"
                   :chart-options="chartOptions"
                   height="300"/>
        <p v-else class="text-muted mb-0">Pas de données.</p>
      </div>
    </div>

    <!-- Carte ------------------------------------------------------>
    <div class="card">
      <div class="card-header">Carte de France</div>
      <div class="card-body p-0">
        <div id="map" style="height:400px"></div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import axios        from 'axios'
import L            from 'leaflet'
import Indicator    from '@/components/Indicator.vue'

/* Chart.js ------------------------------------------------------ */
import { Line as LineChart } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement,
         LineElement, Tooltip } from 'chart.js'
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip)

/* Villes dispo -------------------------------------------------- */
const cities = [
  { name:'Paris',      lat:48.8566, lon:2.3522 },
  { name:'Lyon',       lat:45.7578, lon:4.832 },
  { name:'Marseille',  lat:43.2965, lon:5.3698 },
  { name:'Bordeaux',   lat:44.8378, lon:-0.5792 },
  { name:'Lille',      lat:50.6292, lon:3.0573 }
]

/* État ---------------------------------------------------------- */
const selectedCityName = ref(cities[0].name)
const selectedCity = computed(() => cities.find(c => c.name === selectedCityName.value))

const weatherData = ref(null)
const error       = ref(null)

/* Fetch météo --------------------------------------------------- */
async function fetchWeatherData () {
  error.value = null
  try {
    const { lat, lon } = selectedCity.value
    const { data } = await axios.get('http://localhost:8000/api/weather', {
      params: { lat, lon }
    })
    weatherData.value = data
  } catch {
    error.value = 'Impossible de récupérer les données météo'
  }
}

/* Mise à jour à chaque changement + immédiat -------------------- */
watch(selectedCityName, async () => {
  await fetchWeatherData()
  if (map) map.setView([selectedCity.value.lat, selectedCity.value.lon], 9)
}, { immediate:true })

/* Leaflet ------------------------------------------------------- */
let map
onMounted(() => {
  map = L.map('map').setView([46.6, 1.8], 6)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:'© OpenStreetMap'
  }).addTo(map)

  cities.forEach(c => {
    L.marker([c.lat, c.lon]).addTo(map)
      .bindPopup(c.name)
      .on('click', () => { selectedCityName.value = c.name })
  })
})

/* Computed indicateurs ----------------------------------------- */
const temperature  = computed(() => weatherData.value?.current?.temperature_2m ?? '--')
const humidity     = computed(() => weatherData.value?.current?.relative_humidity_2m ?? '--')
const wind         = computed(() => weatherData.value?.current?.wind_speed_10m ?? '--')
const precipToday  = computed(() => weatherData.value?.daily?.precipitation_sum?.[0] ?? '--')

/* Graph précipitations ----------------------------------------- */
const rainChart = computed(() => {
  if (!weatherData.value?.daily?.precipitation_sum?.length) return { datasets: [] }
  return {
    labels: weatherData.value.daily.time.map(d => d.slice(5)),   // ex : 05-26
    datasets:[{
      label:'Pluie (mm)',
      data: weatherData.value.daily.precipitation_sum,
      borderColor:'#0d6efd',
      backgroundColor:'#0d6efd33',
      tension:.3,
      fill:true
    }]
  }
})
const chartOptions = { responsive:true, maintainAspectRatio:false }
</script>
