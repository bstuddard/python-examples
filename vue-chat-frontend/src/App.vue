<template>
  <router-view :key="$route.fullPath"></router-view>
</template>


<script setup lang="ts">
import { onMounted } from 'vue';
import { devlog } from './devlogger/devlogger';



// Log startup
onMounted(async () => {

  // Try to auth user
  devlog('Running main App.vue.')

});



</script>

