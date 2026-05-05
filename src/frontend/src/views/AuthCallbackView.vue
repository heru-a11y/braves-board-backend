<template>
  <div class="h-screen flex items-center justify-center">
    <p class="text-gray-600">Redirecting...</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  // 🔥 langsung arahkan ke dashboard
  router.replace('/dashboard')
})
</script>