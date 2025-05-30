<template>
  <div>
    <h3 class="font-semibold text-gray-500 mb-4">Chatbot exportieren</h3>
    <p class="text-gray-600 text-sm mb-2">Nutze den folgenden Code, um den Chatbot als iFrame in eine beliebige Website einzubetten.</p>
    <div class="flex flex-col gap-4">
      <div class="bg-gray-100 p-4 rounded-lg">
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-medium text-gray-600">Code zum Einbetten:</span>
          <Button icon="pi pi-copy" 
                  @click="copyIframeCode"
                  class="p-button-text p-button-sm" />
        </div>
        <pre class="block w-full text-sm bg-white p-3 rounded border font-mono whitespace-pre overflow-x-auto select-all cursor-pointer" @click="copyIframeCode">{{ iframeCode }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, ref, isRef, onMounted } from 'vue'
import Button from 'primevue/button'

const agentId = inject('agentId')
const iframeCode = ref('')
const agentIdRef = isRef(agentId) ? agentId : ref(agentId)

onMounted(() => {
  if (agentIdRef.value) {
    const src = `http://localhost:8000/embed/get/${agentIdRef.value}`
    iframeCode.value = ` <iframe
  src="${src}"
  id="chatbot-iframe"
  style="
    position: fixed;
    bottom: 10px;
    right: 10px;
    border: none;
    z-index: 999999;
  "
  width="360"   
  height="550"  
></iframe>`
  }})

function copyIframeCode() {
  navigator.clipboard.writeText(iframeCode.value)
}
</script>
