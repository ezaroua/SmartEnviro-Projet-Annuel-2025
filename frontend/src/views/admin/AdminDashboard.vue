<template>
  <h2 class="mb-4">Admin – Vue d'ensemble</h2>
  <div class="row g-3">
    <Indicator color="info"  icon="bi-people"       label="Utilisateurs" :value="users"/>
    <Indicator color="success" icon="bi-geo-alt"    label="Stations"     :value="stations"/>
    <Indicator color="danger" icon="bi-exclamation" label="Alertes 24h"  :value="alerts"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Indicator from '@/components/Indicator.vue'
const users = ref(123)
const stations = ref(27)
const alerts = ref(3)
</script>
