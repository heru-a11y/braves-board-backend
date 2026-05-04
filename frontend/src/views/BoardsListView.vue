<template>
  <Layout>
    <div class="p-6">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-xl font-bold text-gray-800">My Boards</h1>
        <button @click="showCreate = true"
          class="bg-blue-500 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-600 transition">
          + New Board
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-sm text-gray-400">Loading boards...</div>

      <!-- Empty -->
      <div v-else-if="boards.length === 0" class="text-sm text-gray-400">
        No boards yet. Create one!
      </div>

      <!-- Board Grid -->
      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div v-for="board in boards" :key="board.id" @click="router.push(`/boards/${board.id}`)"
          class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 cursor-pointer hover:shadow-lg transition text-white aspect-video flex flex-col justify-between">
          <h3 class="font-semibold text-sm">{{ board.title }}</h3>
          <p class="text-xs text-blue-100">Click to open</p>
        </div>
      </div>

      <!-- Create Board Modal -->
      <div v-if="showCreate" class="fixed inset-0 z-50 flex items-center justify-center"
        style="background: rgba(0,0,0,0.5)" @click.self="showCreate = false">
        <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm mx-4">
          <h2 class="text-base font-bold text-gray-800 mb-4">Create Board</h2>
          <input v-model="newTitle" @keyup.enter="handleCreate" placeholder="Board title..." autofocus
            class="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 outline-none focus:border-blue-400 transition mb-3" />
          <div class="flex gap-2">
            <button @click="handleCreate" :disabled="creating || !newTitle.trim()"
              class="flex-1 bg-blue-500 text-white text-sm py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 transition">
              {{ creating ? 'Creating...' : 'Create' }}
            </button>
            <button @click="showCreate = false; newTitle = ''" class="text-sm text-gray-400 px-3 hover:text-gray-600">
              Cancel
            </button>
          </div>
        </div>
      </div>

      <!-- Toast -->
      <Teleport to="body">
        <Transition name="toast">
          <div v-if="toast"
            class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[60] bg-gray-900 text-white text-sm px-5 py-2.5 rounded-xl shadow-lg pointer-events-none">
            {{ toast }}
          </div>
        </Transition>
      </Teleport>
    </div>
  </Layout>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Layout from '../components/AppLayout.vue'
import { useAppStore } from '../store/appStore'
import { storeToRefs } from 'pinia'

const router = useRouter()
const store = useAppStore()
const { boards } = storeToRefs(store)

const loading = ref(false)
const creating = ref(false)
const showCreate = ref(false)
const newTitle = ref('')
const toast = ref('')
let toastTimer: ReturnType<typeof setTimeout> | null = null

function showToast(msg: string) {
  toast.value = msg
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.value = '' }, 2500)
}

async function fetchBoards() {
  loading.value = true
  try {
    await store.fetchBoards()  // ← tidak fetch ulang kalau sudah ada
  } catch {
    showToast('Gagal memuat boards.')
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  if (!newTitle.value.trim() || creating.value) return
  creating.value = true
  try {
    const board = await store.addBoard(newTitle.value.trim())
    newTitle.value = ''
    showCreate.value = false
    showToast(`Board "${board.title}" created!`)
  } catch {
    showToast('Gagal membuat board.')
  } finally {
    creating.value = false
  }
}

onMounted(fetchBoards)
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(12px);
}
</style>