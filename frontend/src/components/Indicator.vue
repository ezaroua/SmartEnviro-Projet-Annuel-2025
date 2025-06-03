<template>
  <div class="col-6 col-md-4 col-lg-3">
    <div :class="['card text-white h-100 bg-'+color]">
      <div class="card-body d-flex flex-column justify-content-between">
        <div><i :class="['bi', icon, 'me-2']"></i>{{ label }}</div>
        <div class="fs-3 fw-bold">{{ value }}</div>
      </div>
    </div>
  </div>
</template>
<script setup>
defineProps({ color:String, icon:String, label:String, value:String })
</script>
