<template>
  <div class="flex flex-col p-8">
    <h1 class="text-3xl font-bold mb-2">Vorgänge</h1>
    <span class="text-gray-500 mb-6">Alle Support-Vorgänge im Überblick</span>
    <div class="mb-8 w-full lg:w-1/2">
      <div class="flex items-center border rounded-lg bg-white px-4 py-2 gap-2">
        <i class="pi pi-search text-gray-400"></i>
        <InputText
          v-model="search"
          type="text"
          class="flex-1 bg-transparent outline-none border-0 shadow-none"
          placeholder="Suche nach Vorgängen..."
        />
      </div>
    </div>
    <DataTable
      :value="items"
      :paginator="true"
      :rows="15"
      :sortField="'createdAt'"
      :sortOrder="-1"
      :globalFilterFields="['origin','topic','status','createdAt']"
      :globalFilter="search"
      selectionMode="single"
      dataKey="id"
      class="border rounded-xl bg-white shadow"
      @rowClick="goToDetails"
      style="cursor:pointer;"
    >
      <Column field="origin" header="Vorgänge" :sortable="true">
        <template #body="{ data }">
          <span class="font-semibold">{{ data.origin }}</span>
        </template>
      </Column>
      <Column field="topic" header="Thema" :sortable="true">
        <template #body="{ data }">
          <span>{{ data.topic }}</span>
        </template>
      </Column>
      <Column field="status" header="Status" :sortable="true">
        <template #body="{ data }">
          <Tag :value="data.status" :severity="statusSeverity(data.status)" class="text-white font-semibold text-sm px-4 py-2 rounded-full" />
        </template>
      </Column>
      <Column field="createdAt" header="Erstellt am" :sortable="true">
        <template #body="{ data }">
          {{ formatDate(data.createdAt) }}
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'

const router = useRouter()
const search = ref('')
const items = ref([
  { id: 1, origin: 'E-Mail', topic: 'Rechnung', status: 'Offen', createdAt: '2025-05-20' },
  { id: 2, origin: 'Chat', topic: 'Rücksendung', status: 'In Bearbeitung', createdAt: '2025-05-21' },
  { id: 3, origin: 'Telefon', topic: 'Technische Frage', status: 'Abgeschlossen', createdAt: '2025-05-18' },
  { id: 4, origin: 'Chat', topic: 'Lieferung', status: 'Offen', createdAt: '2025-05-22' },
  { id: 5, origin: 'E-Mail', topic: 'Konto', status: 'Abgeschlossen', createdAt: '2025-05-17' },
  { id: 6, origin: 'Telefon', topic: 'Reklamation', status: 'In Bearbeitung', createdAt: '2025-05-19' }
])

function statusSeverity(status) {
  switch (status) {
    case 'Offen': return 'info'
    case 'In Bearbeitung': return 'warning'
    case 'Abgeschlossen': return 'success'
    default: return 'secondary'
  }
}
function formatDate(date) {
  return new Date(date).toLocaleDateString('de-DE', { year: 'numeric', month: '2-digit', day: '2-digit' })
}
function goToDetails({ data }) {
  const id = data?.id
  if (id) {
    router.push({ name: 'vorgang-details', params: { id } })
  }
}
</script>

<style scoped>
</style>