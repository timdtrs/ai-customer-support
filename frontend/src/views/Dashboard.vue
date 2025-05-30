<template>
  <div class="flex flex-col p-8"> 
    <h1 class="text-3xl font-bold mb-2">Dashboard</h1>
    <span class="text-gray-500 mb-6">Übersicht über die Performance des Chatbots</span>
    <div class="flex flex-row gap-6 mt-8">
      <div class="info-card flex flex-col p-6 flex-1 bg-gray-100 rounded-xl shadow">
        <h6 class="text-sm font-semibold mb-1 text-gray-500">Chats insgesamt</h6>
        <span class="text-3xl font-bold">1271</span>
      </div>
      <div class="info-card flex flex-col p-6 flex-1 bg-gray-100 rounded-xl shadow">
        <h6 class="text-sm font-semibold mb-1 text-gray-500">Kundenzufriedenheit</h6>
        <span class="text-3xl font-bold">92%</span>
      </div>
      <div class="info-card flex flex-col p-6 flex-1 bg-gray-100 rounded-xl shadow">
        <h6 class="text-sm font-semibold mb-1 text-gray-500">Offene Vorgänge</h6>
        <span class="text-3xl font-bold">21</span>
      </div>
    </div>
    <h4 class="font-semibold text-xl mt-10 mb-4">Statistiken</h4>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="bg-white rounded-xl shadow p-6">
        <h5 class="font-semibold mb-4">Chats der letzten 30 Tage</h5>
        <Chart type="line" :data="chatsChartData" :options="chatsChartOptions" class="w-full" />
      </div>
      <div class="bg-white rounded-xl shadow p-6">
        <h5 class="font-semibold mb-4">Erfolgsrate der letzten 30 Tage</h5>
        <Chart type="bar" :data="successChartData" :options="successChartOptions" class="w-full" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from 'primevue/chart';

const chatsChartData = ref({});
const chatsChartOptions = ref({});
const successChartData = ref({});
const successChartOptions = ref({});

onMounted(() => {
  // Dummy-Daten für die letzten 30 Tage
  const days = Array.from({ length: 30 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (29 - i));
    return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit' });
  });
  const chats = Array.from({ length: 30 }, () => Math.floor(Math.random() * 80 + 20));
  const success = Array.from({ length: 30 }, () => Math.floor(Math.random() * 20 + 80));

  chatsChartData.value = {
    labels: days,
    datasets: [
      {
        label: 'Chats',
        data: chats,
        fill: true,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4
      }
    ]
  };
  chatsChartOptions.value = {
    plugins: {
      legend: { labels: { color: '#374151' } }
    },
    scales: {
      x: { ticks: { color: '#6b7280' }, grid: { color: '#f3f4f6' } },
      y: { beginAtZero: true, ticks: { color: '#6b7280' }, grid: { color: '#f3f4f6' } }
    }
  };

  successChartData.value = {
    labels: days,
    datasets: [
      {
        label: 'Erfolgsrate (%)',
        data: success,
        backgroundColor: '#22c55e',
        borderRadius: 6
      }
    ]
  };
  successChartOptions.value = {
    plugins: {
      legend: { labels: { color: '#374151' } }
    },
    scales: {
      x: { ticks: { color: '#6b7280' }, grid: { color: '#f3f4f6' } },
      y: { beginAtZero: true, max: 100, ticks: { color: '#6b7280' }, grid: { color: '#f3f4f6' } }
    }
  };
});
</script>

<style scoped>
.info-card {
  background-color: #eef1f5;
  border-radius: 10px;
}
</style>