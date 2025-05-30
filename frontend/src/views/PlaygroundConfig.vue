<template>
  <div>
    <label for="model-select" class="block font-semibold text-gray-500 mb-1">Sprachmodell</label>
    <Select id="model-select" v-model="selectedModel" :options="modelOptions" optionLabel="label" optionValue="value" class="w-1/2" />
    <div class="flex flex-col mt-6">
      <div class="flex justify-between items-center mb-1 w-1/2">
        <label for="temperature" class="font-semibold text-gray-500">Temperatur</label>
        <span id="temp-value">{{ temperature }}</span>
      </div>
      <Slider v-model="temperature" :min="0" :max="1" :step="0.1" class="w-1/2" />
    </div>
    <div class="mt-6">
      <label for="system-message" class="block font-semibold text-gray-500 mb-1">Systemanweisung</label>
      <Textarea v-model="systemMessage" class="h-60 w-full" rows="5" cols="30" placeholder="Systemanweisung für das Modell..." style="resize: none;"/>
    </div>
    <Button icon="pi pi-save" label="Speichern" class="mt-2 w-1/3 self-start flex items-center justify-center gap-2" />
  </div>
</template>

<script setup>
import { inject } from 'vue'
import Select from 'primevue/select'
import Slider from 'primevue/slider'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'

const selectedModel = inject('selectedModel')
const modelOptions = inject('modelOptions')
const temperature = inject('temperature')
const systemMessage = inject('systemMessage')
</script>
