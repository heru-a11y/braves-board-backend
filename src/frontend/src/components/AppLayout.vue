<template>
  <div class="flex flex-col h-screen bg-gray-100">
    <!-- TOP HEADER -->
    <div class="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-6 flex-shrink-0 relative">
      <div class="flex items-center gap-2 text-lg font-semibold">
        <img src="../assets/Grid.png" alt="logo" class="w-5" />
        <span class="text-gray-800">Braves</span>
        <span class="text-blue-600">Board</span>
      </div>

      <div class="flex items-center gap-3">
        <button class="w-8 h-8 flex items-center justify-center rounded-full border border-gray-300 hover:bg-gray-50 transition text-gray-600">
          <font-awesome-icon icon="question" class="text-sm" />
        </button>
        <button class="w-8 h-8 flex items-center justify-center rounded-full border border-gray-300 hover:bg-gray-50 transition text-gray-600">
          <font-awesome-icon icon="bell" class="text-sm" />
        </button>
        <button class="w-8 h-8 flex items-center justify-center rounded-full border border-gray-300 hover:bg-gray-50 transition text-gray-600">
          <font-awesome-icon icon="user" class="text-sm" />
        </button>
      </div>

      <!-- REMINDER NOTIFICATION POPUP -->
      <Transition name="reminder">
        <div
          v-if="showReminder"
          class="absolute top-14 right-4 z-50 bg-white rounded-xl shadow-lg border border-gray-200 p-4 w-72"
        >
          <p class="text-xs font-semibold text-gray-500 mb-1">Reminder Notification</p>
          <p class="text-sm text-gray-700 leading-snug">
            you have been working on
            <span class="text-blue-500 font-medium">{{ reminder.task }}</span>
            for {{ reminder.duration }}. Still working on it?
          </p>
          <div class="flex gap-2 mt-3">
            <button
              @click="handleYes"
              class="px-4 py-1.5 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition text-gray-700"
            >
              yes
            </button>
            <button
              @click="handleNo"
              class="px-4 py-1.5 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition text-gray-700"
            >
              No
            </button>
          </div>
        </div>
      </Transition>
    </div>

    <div class="flex flex-1 overflow-hidden">
      <AppSidebar />
      <main class="flex-1 overflow-auto p-6 bg-gray-100">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faQuestion, faBell, faUser } from '@fortawesome/free-solid-svg-icons'
import AppSidebar from './AppSidebar.vue'

library.add(faQuestion, faBell, faUser)

// ── Reminder state ────────────────────────────────────────────────────────────

const showReminder = ref(false)

const reminder = ref({
  task: 'Snap Journal - Fixing some bu..',
  duration: '3 hours',
})

// Dummy reminders pool — bisa diganti data real
const reminders = [
  { task: 'Snap Journal - Fixing some bu..', duration: '3 hours' },
  { task: 'Braves Board - UI Revamp..', duration: '1.5 hours' },
  { task: 'FS Internship - API Integration..', duration: '2 hours' },
]

let reminderTimer: ReturnType<typeof setTimeout> | null = null

function showNextReminder() {
  const random = reminders[Math.floor(Math.random() * reminders.length)]
  reminder.value = random
  showReminder.value = true
}

function scheduleNext() {
  // Tampil lagi setiap 30 detik (ganti ke interval yang sesuai di production)
  reminderTimer = setTimeout(() => {
    showNextReminder()
  }, 30_000)
}

function handleYes() {
  showReminder.value = false
  scheduleNext()
}

function handleNo() {
  showReminder.value = false
  scheduleNext()
}

onMounted(() => {
  // Tampil pertama kali setelah 3 detik
  reminderTimer = setTimeout(() => {
    showNextReminder()
  }, 3_000)
})

onUnmounted(() => {
  if (reminderTimer) clearTimeout(reminderTimer)
})
</script>

<style scoped>
.reminder-enter-active,
.reminder-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.reminder-enter-from,
.reminder-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>