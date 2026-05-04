<template>
  <AppLayout>
    <h2 class="text-xl font-semibold text-gray-800 mb-5">Projects</h2>

    <div class="bg-white border border-gray-200 rounded-lg flex items-center gap-0 mb-4 overflow-hidden">
      <span class="px-4 py-2.5 text-sm text-gray-400 border-r border-gray-200">Filter</span>
      <button
        v-for="label in filterLabels"
        :key="label"
        class="flex items-center gap-1 px-4 py-2.5 text-sm text-gray-600 border-r border-gray-200 hover:bg-gray-50 transition"
      >
        {{ label }}
        <svg class="w-3 h-3 text-gray-400 ml-0.5" viewBox="0 0 10 6" fill="currentColor">
          <path d="M0 0l5 6 5-6z"/>
        </svg>
      </button>
      <div class="flex items-center gap-2 flex-1 px-4 py-2.5">
        <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
        </svg>
        <input
          type="text"
          placeholder="Find by name"
          v-model="search"
          class="text-sm outline-none bg-transparent text-gray-600 w-full placeholder-gray-400"
        />
      </div>
      <button class="px-4 py-2.5 text-sm font-medium text-gray-700 border-l border-gray-200 hover:bg-gray-50 transition whitespace-nowrap">
        apply filter
      </button>
    </div>

    <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="bg-gray-100 px-6 py-2 text-sm font-medium text-gray-600 border-b border-gray-200">
        Projects
      </div>
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-200">
            <th
              v-for="col in cols"
              :key="col.key"
              @click="handleSort(col.key)"
              class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer select-none hover:text-gray-700"
            >
              {{ col.label }}
              <svg class="inline ml-1 w-3 h-3 text-gray-500" viewBox="0 0 10 14" fill="currentColor">
                <path d="M5 0L9.33 5H0.67L5 0Z"/>
                <path d="M5 14L0.67 9H9.33L5 14Z" opacity="0.4"/>
              </svg>
            </th>
            <th class="px-6 py-3 w-10"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="project in filtered"
            :key="project.id"
            class="border-b border-gray-100 hover:bg-gray-50 transition"
          >
            <td class="px-6 py-3">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full flex-shrink-0" :class="project.color"></span>
                <span class="text-gray-800">{{ project.name }}</span>
              </div>
            </td>
            <td class="px-6 py-3 text-gray-500">{{ project.client }}</td>
            <td class="px-6 py-3 text-gray-700">{{ project.tracked }}</td>
            <td class="px-6 py-3 text-gray-500">{{ project.progress }}</td>
            <td class="px-6 py-3 text-gray-700">{{ project.access }}</td>
            <td class="px-6 py-3 text-right">
              <button @click="toggleStar(project.id)" :title="project.starred ? 'Remove from favorites' : 'Add to favorites'">
                <svg v-if="project.starred" class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                <svg v-else class="w-5 h-5 text-gray-300 hover:text-yellow-400 transition" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </button>
            </td>
          </tr>
          <tr v-if="filtered.length === 0">
            <td colspan="6" class="px-6 py-12 text-center text-gray-400 text-sm">
              No projects found.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import type { Project } from '../types'

const filterLabels: string[] = ['Active', 'Client', 'Access']

const projects = ref<Project[]>([
  { id: 1, name: 'FS Internship', client: '-', tracked: '261,8h', progress: '-', access: 'Public', starred: true,  color: 'bg-green-500' },
  { id: 2, name: 'BE Internship', client: '-', tracked: '282,2h', progress: '-', access: 'Public', starred: false, color: 'bg-blue-400' },
])

const search  = ref<string>('')
const sortKey = ref<keyof Project | null>(null)
const sortDir = ref<number>(1)

const cols: { label: string; key: keyof Project }[] = [
  { label: 'NAME',     key: 'name' },
  { label: 'CLIENT',   key: 'client' },
  { label: 'TRACKED',  key: 'tracked' },
  { label: 'PROGRESS', key: 'progress' },
  { label: 'ACCESS',   key: 'access' },
]

function toggleStar(id: number): void {
  const p = projects.value.find(p => p.id === id)
  if (p) p.starred = !p.starred
}

function handleSort(key: keyof Project): void {
  if (sortKey.value === key) sortDir.value *= -1
  else { sortKey.value = key; sortDir.value = 1 }
}

const filtered = computed<Project[]>(() => {
  const sorted = [...projects.value].sort((a, b) => {
    if (a.starred !== b.starred) return a.starred ? -1 : 1
    if (!sortKey.value) return 0
    const av = String(a[sortKey.value] ?? '')
    const bv = String(b[sortKey.value] ?? '')
    return av < bv ? -sortDir.value : av > bv ? sortDir.value : 0
  })
  return sorted.filter(p =>
    p.name.toLowerCase().includes(search.value.toLowerCase())
  )
})
</script>