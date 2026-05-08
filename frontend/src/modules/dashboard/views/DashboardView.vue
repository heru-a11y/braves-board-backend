<template>
  <AppLayout>
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Dashboard</h1>
      <!-- <p class="text-sm text-gray-500 mt-1">Welcome back, {{ user?.full_name ?? '...' }}</p> -->
      <p class="text-base font-semibold text-gray-700 mt-3">
        Manage Tasks and Track Time Efficiently
      </p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-xl border border-gray-200 p-4">
        <p class="text-xs text-gray-400 mb-1">Total Boards</p>
        <p class="text-2xl font-bold text-gray-800">{{ stats.boards }}</p>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-4">
        <p class="text-xs text-gray-400 mb-1">Total Tasks</p>
        <p class="text-2xl font-bold text-gray-800">{{ stats.tasks }}</p>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-4">
        <p class="text-xs text-gray-400 mb-1">Completed</p>
        <p class="text-2xl font-bold text-emerald-500">{{ stats.completed }}</p>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-4">
        <p class="text-xs text-gray-400 mb-1">In Progress</p>
        <p class="text-2xl font-bold text-blue-500">{{ stats.inProgress }}</p>
      </div>
    </div>

    <!-- Quick actions -->
    <div>
      <h2 class="text-sm font-semibold text-gray-700 mb-4">Quick Actions</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
        <router-link to="/boards"
          class="bg-white rounded-xl border border-gray-200 p-4 hover:border-blue-400 hover:shadow-sm transition flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
            <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-700">Boards</p>
            <p class="text-xs text-gray-400">Manage your boards</p>
          </div>
        </router-link>

        <router-link to="/tracker"
          class="bg-white rounded-xl border border-gray-200 p-4 hover:border-blue-400 hover:shadow-sm transition flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center">
            <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-700">Time Tracker</p>
            <p class="text-xs text-gray-400">Track your time</p>
          </div>
        </router-link>

        <router-link to="/reports"
          class="bg-white rounded-xl border border-gray-200 p-4 hover:border-blue-400 hover:shadow-sm transition flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-purple-50 flex items-center justify-center">
            <svg class="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-700">Reports</p>
            <p class="text-xs text-gray-400">View your reports</p>
          </div>
        </router-link>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '../../../components/common/AppLayout.vue'
import { useAppStore } from '../../board/store/board.store'
import { storeToRefs } from 'pinia'
import api from '../../../app/api'

interface User {
  id: string
  email: string
  full_name: string
  picture_url?: string
}

const user = ref<User | null>(null)
const loading = ref(false)
const store = useAppStore()
const { boards } = storeToRefs(store)

const stats = computed(() => {
  let tasks = 0
  let completed = 0
  let inProgress = 0

  for (const board of boards.value) {
    // boards di sini adalah list boards, bukan columns
    tasks += 0
  }

  return { boards: boards.value.length, tasks, completed, inProgress }
})

onMounted(async () => {
  // load user
  try {
    const savedUser = localStorage.getItem('user')
    if (savedUser) user.value = JSON.parse(savedUser)
    const res = await api.get('/auth/me')
    user.value = res.data?.data ?? res.data
  } catch { }

  // load boards
  loading.value = true
  try {
    await store.fetchBoards()
  } catch { } finally {
    loading.value = false
  }
})
</script>