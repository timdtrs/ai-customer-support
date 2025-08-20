<template>
  <div class="w-3/4">
    <div class="mt-8 flex flex-col">
      <h5 class="font-semibold mb-3">Dateien hochladen</h5>
      <div class="flex flex row">
        <FileUpload 
          mode="basic" 
          name="demo[]" 
          :auto="true" 
          :customUpload="true"
          @uploader="handleFileUploadPrime"
          chooseLabel="Dateien auswählen"
          class="w-full h-10 mb-2"
        />
        <Button :disabled="deleteFiles.length == 0" class="h-10 ms-2" icon="pi pi-trash" label="Ausgewählte löschen" severity="secondary" @click="removeSelectedFiles" />
      </div>
      <h5 class="font-semibold mt-6">Deine Dateien</h5>
      <DataTable v-model:selection="deleteFiles" :value="uploadedFiles" dataKey="id" selectionMode="multiple" class="w-3/4">
        <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
        <Column field="name" header="Dateiname"></Column>
        <Column field="size" header="Größe (KB)"></Column>
        <Column field="status" header="Status"></Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import FileUpload from 'primevue/fileupload'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import { indexFilesInVectorDB, getIndexedFiles, deleteIndexedFile } from '@/api/index'
import { useAuth0 } from '@auth0/auth0-vue'

const uploadedFiles = defineModel('uploadedFiles', { type: Array, required: true })
const deleteFiles = defineModel('deleteFiles', { type: Array, required: true })

function handleFileUploadPrime(event) {
  if (event.files && event.files.length) {
    const newFiles = event.files.map(file => ({
      id: file.name,
      name: file.name,
      size: Math.ceil(file.size / 1024), // Größe in KB
      status: 'Neu',
      file
    }))
    uploadedFiles.value.push(...newFiles)
  }
}

async function removeSelectedFiles() {
  const token = await getAccessTokenSilently({
    audience: import.meta.env.VITE_AUTH0_AUDIENCE,
  }).catch(() => null)
  for (const file of deleteFiles.value) {
    if (file.status === 'Indiziert') {
      try {
        await deleteIndexedFile(file.name, token)
      } catch (e) {
        console.log('Fehler beim Löschen aus dem Vektorstore:', e)
      }
    }
  }
  uploadedFiles.value = uploadedFiles.value.filter(file => !deleteFiles.value.includes(file))
  deleteFiles.value = []
}

onMounted(async () => {
  try {
    const token = await getAccessTokenSilently({
      audience: import.meta.env.VITE_AUTH0_AUDIENCE,
    }).catch(() => null)
    const indexed = await getIndexedFiles(token);
    uploadedFiles.value.forEach(file => {
      const found = indexed.find(f => f.title === file.name)
      if (found) file.status = 'Indiziert'
    })
    indexed.forEach(f => {
      if (!uploadedFiles.value.some(file => file.name === f.title)) {
        uploadedFiles.value.push({
          id: `${f.title}_indexed`,
          name: f.title,
          size: f.size,
          status: 'Indiziert',
          file: null
        })
      }
const { getAccessTokenSilently } = useAuth0()
    })
  } catch (e) {
    // Fehlerbehandlung optional
  }
})
</script>
