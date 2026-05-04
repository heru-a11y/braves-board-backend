<template>
  <AppLayout>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-gray-700">
        Manage Tasks and Track Time Efficiently
      </h2>
      <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow">
        + Create New Board
      </button>
    </div>

    <!-- USER INFO -->
    <div v-if="user" class="mb-6 p-4 bg-white rounded-xl shadow border">
      <p class="text-gray-700 font-medium">Welcome, {{ user.full_name }}</p>
      <p class="text-sm text-gray-500">{{ user.email }}</p>
    </div>

    <!-- CARD -->
    <div class="bg-white w-60 p-4 rounded-xl shadow border">
      <h3 class="font-semibold text-gray-800 mb-2">First Board</h3>
      <p class="text-sm text-gray-500">0 tasks</p>
      <p class="text-xs text-gray-400 mt-2">Total Time : 0s</p>
    </div>
  </AppLayout>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import api from '../services/api'

interface User {
  id: string
  email: string
  full_name: string
  picture_url?: string
}

const user = ref<User | null>(null)

onMounted(async () => {
  try {
    const res = await api.get('/auth/me')
    user.value = res.data.data
  } catch (err) {
  localStorage.removeItem('access_token')
  // window.location.href = '/'
  console.log('TOKEN:', localStorage.getItem('access_token')) 
  console.log('RESPONSE:', )
}
})
</script>