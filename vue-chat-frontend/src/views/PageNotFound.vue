<template>
    <BackgroundWrapper>
        <div class="p-7 flex flex-col items-center jusitify-center space-y-6">
            <h1 class="text-5xl font-extrabold">404</h1>
            <h2 class="text-2xl font-semibold mt-2">Page not found</h2>
            <p class="text-lg">The page you are looking for does not exist.</p>
            <router-link to="/" class="button bg-emerald-50 text-emerald-950 font-semibold mx-2 py-2 px-4 rounded-md cursor-pointer sm:hover:bg-emerald-200 sm:transition">Return to Home</router-link>
        </div>
    </BackgroundWrapper>
</template>

<script setup lang="ts">
import BackgroundWrapper from '@/components/backgrounds/BackgroundWrapper.vue';
</script>