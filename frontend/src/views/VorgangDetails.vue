<template>
  <div class="flex flex-col p-8">
    <h1 class="text-3xl font-bold mb-2">Vorgang #{{ vorgang.id }}</h1>
    <div class="flex flex-row gap-8 mt-8">
      <div class="flex flex-col p-6 rounded-2xl bg-gray-100 min-w-[340px] max-w-[400px]">
        <h5 class="font-semibold mb-2">Informationen</h5>
        <div class="mb-6">
          <div class="flex flex-row gap-6">
            <div class="flex flex-col mt-2 w-1/2">
              <span class="font-semibold text-gray-500">Herkunft</span>
              <span class="font-semibold">{{ vorgang.origin }}</span>
            </div>
            <div class="flex flex-col mt-2 w-1/2">
              <span class="font-semibold text-gray-500">Status</span>
              <span class="px-4 py-2 rounded-full text-white text-sm font-semibold mt-1" :class="statusClass(vorgang.status)">{{ vorgang.status }}</span>
            </div>
          </div>
          <div class="flex flex-row gap-6">
            <div class="flex flex-col mt-2 w-1/2">
              <span class="font-semibold text-gray-500">Thema</span>
              <span class="font-semibold">{{ vorgang.topic }}</span>
            </div>
            <div class="flex flex-col mt-2 w-1/2">
              <span class="font-semibold text-gray-500">Erstellt am</span>
              <span class="font-semibold">{{ formatDate(vorgang.createdAt) }}</span>
            </div>
          </div>
        </div>
        <h5 class="font-semibold mt-6">Zusammenfassung</h5>
        <p class="text-gray-500 max-w-xs">Hier steht eine Zusammenfassung des bisherigen Vorgangs.</p>
      </div>
      <div class="flex-1 flex flex-col justify-start items-stretch bg-white rounded-2xl shadow p-6 min-w-[350px] max-w-[600px] min-h-[420px]">
        <h5 class="font-semibold mb-3 text-base">Chatverlauf</h5>
        <div class="flex flex-col flex-grow rounded-2xl p-4 bg-gray-100 min-h-[300px] max-h-[60vh] overflow-auto">
          <div class="flex-grow mb-3 overflow-auto max-h-80" ref="messagesEnd">
            <div v-for="(msg, idx) in chatMessages" :key="idx" :class="['mb-2 px-3 py-2 rounded-lg', msg.role === 'user' ? 'bg-blue-100 text-blue-900 self-end' : 'bg-gray-700 text-white self-start']">
              <span class="font-semibold">{{ msg.role === 'user' ? 'Kunde' : 'Bot' }}</span>
              <span class="ml-2">{{ msg.text }}</span>
              <span class="ml-2 text-gray-400 text-xs">{{ formatTime(msg.timestamp) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Dummy-Daten wie in Vorgaenge.vue
const items = [
  { id: 1, origin: 'E-Mail', topic: 'Rechnung', status: 'Offen', createdAt: '2025-05-20' },
  { id: 2, origin: 'Chat', topic: 'Rücksendung', status: 'In Bearbeitung', createdAt: '2025-05-21' },
  { id: 3, origin: 'Telefon', topic: 'Technische Frage', status: 'Abgeschlossen', createdAt: '2025-05-18' },
  { id: 4, origin: 'Chat', topic: 'Lieferung', status: 'Offen', createdAt: '2025-05-22' },
  { id: 5, origin: 'E-Mail', topic: 'Konto', status: 'Abgeschlossen', createdAt: '2025-05-17' },
  { id: 6, origin: 'Telefon', topic: 'Reklamation', status: 'In Bearbeitung', createdAt: '2025-05-19' }
]
const vorgang = computed(() => items.find(v => v.id === Number(route.params.id)))
const chatMessages = ref([])
const chatLoaded = ref(false)

onMounted(async () => {
  try {
    // Annahme: Chatverlauf liegt in /src/assets/chatlogs/vorgang_<id>.json
    const res = await fetch(`/src/assets/chatlogs/vorgang_${route.params.id}.json`)
    if (res.ok) {
      chatMessages.value = await res.json()
    }
  } catch (e) {
    // Datei nicht gefunden oder Fehler
  } finally {
    chatLoaded.value = true
  }
})

function statusClass(status) {
  switch (status) {
    case 'Offen': return 'bg-blue-500';
    case 'In Bearbeitung': return 'bg-yellow-500';
    case 'Abgeschlossen': return 'bg-green-500';
    default: return 'bg-gray-500';
  }
}
function formatDate(date) {
  return new Date(date).toLocaleDateString('de-DE', { year: 'numeric', month: '2-digit', day: '2-digit' })
}
function formatTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })
}
function goBack() {
  router.push({ name: 'vorgaenge' })
}
</script>

<style scoped>
.case-open {
  background-color: #3b82f6;
}
.case-pending {
  background-color: #f59e42;
}
.case-done {
  background-color: #22c55e;
}
</style>
