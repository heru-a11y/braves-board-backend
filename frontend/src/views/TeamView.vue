<template>
  <AppLayout>
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Team</h2>

    <div class="flex border-b border-gray-200 mb-4">
      <button
        v-for="t in tabs"
        :key="t"
        @click="activeTab = t"
        class="px-5 py-2.5 text-sm font-medium transition border-b-2 -mb-px"
        :class="activeTab === t
          ? 'border-blue-600 text-blue-600'
          : 'border-transparent text-gray-500 hover:text-gray-700'"
      >
        {{ t }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center h-40 text-gray-400 text-sm gap-2">
      <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
      </svg>
      Loading members...
    </div>

    <template v-if="activeTab === 'Members'" v-show="!loading">
      <div class="bg-white border border-gray-200 rounded-lg flex items-center gap-0 mb-4 overflow-hidden">
        <span class="px-4 py-2.5 text-sm text-gray-400 border-r border-gray-200">Filter</span>
        <button v-for="label in ['All', 'Role', 'Group']" :key="label"
          class="flex items-center gap-1 px-4 py-2.5 text-sm text-gray-600 border-r border-gray-200 hover:bg-gray-50 transition">
          {{ label }}
          <svg class="w-3 h-3 text-gray-400 ml-0.5 inline" viewBox="0 0 10 6" fill="currentColor">
            <path d="M0 0l5 6 5-6z"/>
          </svg>
        </button>
        <div class="flex items-center gap-2 flex-1 px-4 py-2.5">
          <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
          </svg>
          <input type="text" placeholder="Search by name or email" v-model="search"
            class="text-sm outline-none bg-transparent text-gray-600 w-full placeholder-gray-400" />
        </div>
        <button class="px-4 py-2.5 text-sm font-medium text-gray-700 border-l border-gray-200 hover:bg-gray-50 transition whitespace-nowrap">
          apply filter
        </button>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="bg-gray-100 px-6 py-2 text-sm font-medium text-gray-600 border-b border-gray-200">Members</div>
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200">
              <th v-for="label in ['NAME', 'EMAIL', 'ROLE', 'GROUP']" :key="label"
                class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">
                {{ label }}
                <svg v-if="label === 'NAME' || label === 'EMAIL'" class="inline ml-1 w-3 h-3" viewBox="0 0 10 14" fill="currentColor">
                  <path d="M5 0L9.33 5H0.67L5 0Z"/>
                  <path d="M5 14L0.67 9H9.33L5 14Z" opacity="0.4"/>
                </svg>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in filteredMembers" :key="m.id" class="border-b border-gray-100 hover:bg-gray-50 transition">
              <td class="px-6 py-3 text-gray-800 font-medium">{{ m.name }}</td>
              <td class="px-6 py-3">
                <a :href="`mailto:${m.email}`" class="text-blue-500 hover:underline">{{ m.email }}</a>
              </td>
              <td class="px-6 py-3 text-gray-700">{{ m.role }}</td>
              <td class="px-6 py-3">
                <span class="bg-blue-100 text-blue-600 text-xs font-medium px-2.5 py-1 rounded-full">{{ m.group }}</span>
              </td>
            </tr>
            <tr v-if="filteredMembers.length === 0">
              <td colspan="4" class="px-6 py-12 text-center text-gray-400 text-sm">No members found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <template v-if="activeTab === 'Groups'">
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="bg-gray-100 px-6 py-2 text-sm font-medium text-gray-600 border-b border-gray-200">Groups</div>
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Name</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Members</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="g in groups" :key="g.id" class="border-b border-gray-100 hover:bg-gray-50 transition">
              <td class="px-6 py-3 text-gray-800 font-medium">{{ g.name }}</td>
              <td class="px-6 py-3 text-gray-600">{{ g.members }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { getUsers } from '../services/boardService'
import type { TeamMember, TeamGroup } from '../types'

const tabs: string[] = ['Members', 'Groups']
const activeTab = ref<string>('Members')
const search    = ref<string>('')
const loading   = ref(false)

// Data dari API — groups di-derive dari members
const members = ref<TeamMember[]>([])

const groups = computed<TeamGroup[]>(() => {
  const map: Record<string, number> = {}
  members.value.forEach(m => {
    map[m.group] = (map[m.group] ?? 0) + 1
  })
  return Object.entries(map).map(([name, count], i) => ({
    id: i + 1, name, members: count,
  }))
})

const filteredMembers = computed<TeamMember[]>(() => {
  const q = search.value.toLowerCase()
  return members.value.filter(m =>
    m.name.toLowerCase().includes(q) || m.email.toLowerCase().includes(q)
  )
})

// ─── GET /users ───────────────────────────────────────────────
async function fetchUsers() {
  loading.value = true
  try {
    const raw: any[] = await getUsers()
    // Normalisasi field backend → field TeamMember
    members.value = raw.map((u, i) => ({
      id:    u.id    ?? i,
      name:  u.full_name ?? u.name ?? u.email?.split('@')[0] ?? 'Unknown',
      email: u.email ?? '',
      role:  u.role  ?? '-',
      group: u.group ?? u.team ?? 'General',
    }))
  } catch {
    // Kalau API gagal, biarkan tabel kosong — tidak crash
  } finally {
    loading.value = false
  }
}

onMounted(fetchUsers)
</script>