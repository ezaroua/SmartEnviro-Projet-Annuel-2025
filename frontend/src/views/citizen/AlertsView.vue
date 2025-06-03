<template>
  <h2 class="mb-4">Mes alertes</h2>
  <ul class="list-group">
    <li class="list-group-item" v-for="a in alerts" :key="a.id">
      <span class="badge bg-danger me-2" v-if="a.critical">CRITIQUE</span>
      {{ a.message }} <small class="text-muted">({{ a.date }})</small>
    </li>
  </ul>
</template>

<script setup>
import { ref } from 'vue'
const alerts = ref([
  { id:1, message:'Pic de pollution PM2.5', critical:true,  date:'24 mai 10:32'},
  { id:2, message:'Vent fort prévu demain', critical:false, date:'23 mai 18:10'}
])
</script>
