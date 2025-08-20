<template>
  <div class="flex flex-col p-8">
    <h1 class="text-3xl font-bold mb-2">Wissensbasis</h1>
    <div class="flex flex-row gap-8">
      <div class="flex-1">
        <span class="text-gray-500 mb-6 block">Verwalte deine Wissensdokumente und Frage-Antwort-Paare</span>
        <ul class="flex gap-2 mb-6">
          <li><button class="px-4 py-2 rounded-lg text-sm font-semibold" :class="tab==='files' ? 'files-nav-active' : 'nav-item'" @click="tab='files'">Dateien</button></li>
          <li><button class="px-4 py-2 rounded-lg text-sm font-semibold" :class="tab==='text' ? 'text-nav-active' : 'nav-item' " @click="tab='text'">Text</button></li>
          <li><button class="px-4 py-2 rounded-lg text-sm font-semibold" :class="tab==='qa' ? 'qa-nav-active' : 'nav-item'" @click="tab='qa'">Q&amp;A</button></li>
        </ul>
        <!-- Dateien -->
        <KnowledgeFiles v-if="tab==='files'" v-model:uploadedFiles="uploadedFiles" v-model:deleteFiles="deleteFiles" />
        <!-- Text -->
        <div v-if="tab==='text'">
          <div class="mt-8">
            <h5 class="font-semibold mb-3">Freitext hinzufügen</h5>
            <InputText v-model="textTitle" class="mb-3 w-1/3" placeholder="Titel" />
            <Editor v-model="textInput" editorStyle="height: 220px" class="mb-3" />
            <div class="flex flex-row gap-2">
              <Button severity="danger" label="Speichern" icon="pi pi-save" class="w-1/4 mb-3" @click="saveTextEntry" :disabled="!textTitle.trim() || !textInput.trim()" />
              <Button :disabled="deleteTexts.length == 0" class="h-10 ms-2" icon="pi pi-trash" label="Ausgewählte löschen" severity="danger" @click="removeSelectedTexts" />
            </div>
            <h5 class="font-semibold mt-4">Deine Texte</h5>
            <DataTable v-model:selection="deleteTexts" :value="textEntries" dataKey="id" selectionMode="multiple" class="mt-2 w-3/4">
              <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
              <Column field="title" header="Titel"></Column>
              <Column field="size" header="Größe"></Column>
              <Column header="Aktionen">
                <template #body="slotProps">
                  <Button icon="pi pi-pencil" class="p-button-text p-button-sm mr-2" @click="startEditText(slotProps.data)" />
                </template>
              </Column>
            </DataTable>
            <!-- Edit Dialog für Texte -->
            <Dialog v-model:visible="editTextDialog" modal header="Text bearbeiten" :style="{ width: '450px' }">
              <div class="flex flex-col gap-2">
                <InputText v-model="editTextTitle" placeholder="Titel" />
                <Editor v-model="editTextContent" editorStyle="height: 180px" />
              </div>
              <template #footer>
                <Button label="Abbrechen" icon="pi pi-times" class="p-button-text" @click="editTextDialog=false" />
                <Button label="Speichern" icon="pi pi-check" class="p-button-text" @click="saveEditText" :disabled="!editTextTitle.trim() || !editTextContent.trim()" />
              </template>
            </Dialog>
          </div>
        </div>
        <!-- Q&A -->
        <div v-if="tab==='qa'">
          <div class="mt-8">
            <h5 class="font-semibold mb-3">Q&amp;A hinzufügen</h5>
            <div class="flex flex-col gap-2 mb-3">
              <InputText v-model="qaTitle" class="flex-1 mb-2 w-1/3" placeholder="Titel" />
              <InputText v-model="newQuestion" class="flex-1 mb-2 w-full" placeholder="Frage" />
            </div>
            <Editor v-model="newAnswer" editorStyle="height: 120px" class="mb-3" />
            <div class="flex flex-row gap-2 mb-4">
              <Button label="Speichern" icon="pi pi-save" class="w-1/4" @click="addPair" :disabled="!qaTitle.trim() || !newQuestion.trim() || !newAnswer.trim()" />
              <Button :disabled="deleteQAPairs.length == 0" class="h-10 ms-2" icon="pi pi-trash" label="Ausgewählte löschen" severity="danger" @click="removeSelectedQAPairs" />
            </div>
            <h5 class="font-semibold mt-4">Deine Q&amp;A Einträge</h5>
            <DataTable v-model:selection="deleteQAPairs" :value="qaPairs" dataKey="id" selectionMode="multiple" class="mt-2 w-3/4">
              <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
              <Column field="title" header="Titel"></Column>
              <Column field="question" header="Frage"></Column>
              <Column field="answer" header="Antwort">
                <template #body="slotProps">
                  <div v-html="slotProps.data.answer"></div>
                </template>
              </Column>
              <Column header="Aktionen">
                <template #body="slotProps">
                  <Button icon="pi pi-pencil" class="p-button-text p-button-sm mr-2" @click="startEditQAPair(slotProps.data)" />
                </template>
              </Column>
            </DataTable>
            <!-- Edit Dialog -->
            <Dialog v-model:visible="editQADialog" modal header="Q&amp;A bearbeiten" :style="{ width: '450px' }">
              <div class="flex flex-col gap-2">
                <InputText v-model="editQATitle" placeholder="Titel" />
                <InputText v-model="editQAQuestion" placeholder="Frage" />
                <Editor v-model="editQAAnswer" editorStyle="height: 120px" />
              </div>
              <template #footer>
                <Button label="Abbrechen" icon="pi pi-times" class="p-button-text" @click="editQADialog=false" />
                <Button label="Speichern" icon="pi pi-check" class="p-button-text" @click="saveEditQAPair" :disabled="!editQATitle.trim() || !editQAQuestion.trim() || !editQAAnswer.trim()" />
              </template>
            </Dialog>
          </div>
        </div>
      </div>
      <!-- Übersicht rechts -->
      <div class="bg-white rounded-xl shadow p-6 h-fit min-w-[260px] max-w-[320px] self-start">
        <h5 class="font-semibold mb-3">Wissensbasis-Übersicht</h5>
        <div class="mb-4">
          <ProgressBar :value="usedPercentAll" showValue :style="{height: '18px'}" />
        </div>
        <div>
          <div class="mb-2 flex justify-between items-center">
            <span class="font-semibold text-sm">Dateien</span>
            <span class="text-xs text-gray-500">{{ uploadedFiles.length }} Stück &bull; {{ fileSizeAll }} KB</span>
          </div>
          <div class="mb-2 flex justify-between items-center">
            <span class="font-semibold text-sm">Freitexte</span>
            <span class="text-xs text-gray-500">{{ textEntries.length }} Stück &bull; {{ textSizeAll }} KB</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="font-semibold text-sm">Q&amp;A</span>
            <span class="text-xs text-gray-500">{{ qaPairs.length }} Stück &bull; {{ qaSizeAll }} KB</span>
          </div>
        </div>
        <div class="flex justify-center mt-6">
          <Button label="Trainieren" icon="pi pi-cog" class="w-full" :loading="isTraining" @click="trainKnowledgeBase" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import KnowledgeFiles from '@/components/KnowledgeFiles.vue'
import Editor from 'primevue/editor'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import ProgressBar from 'primevue/progressbar'
import { indexFilesInVectorDB, indexTextsInVectorDB, indexQAPairsInVectorDB, getIndexedFiles, deleteIndexedFile } from '@/api/index'
import { useAuth0 } from '@auth0/auth0-vue'
const tab = ref('files')
const { getAccessTokenSilently } = useAuth0()

// FileUpload
const uploadedFiles = ref([])
const deleteFiles = ref([])

// Text
const textInput = ref('')
const textTitle = ref("")
const savedText = ref(false)
const textEditor = ref(null)
const textEntries = ref([])
const deleteTexts = ref([])
function saveTextEntry() {
  if (!textTitle.value.trim() || !textInput.value.trim()) return
  const entry = {
    id: `${textTitle.value}_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
    title: textTitle.value,
    text: textInput.value
  }
  textEntries.value.push(entry)
  localStorage.setItem('knowledgeTexts', JSON.stringify(textEntries.value))
  textTitle.value = ""
  textInput.value = ""
  savedText.value = true
  setTimeout(() => savedText.value = false, 1200)
}

function removeSelectedTexts() {
  textEntries.value = textEntries.value.filter(entry => !deleteTexts.value.includes(entry))
  deleteTexts.value = []
  localStorage.setItem('knowledgeTexts', JSON.stringify(textEntries.value))
}
// Beim Laden aus LocalStorage lesen
if (localStorage.getItem('knowledgeTexts')) {
  textEntries.value = JSON.parse(localStorage.getItem('knowledgeTexts'))
}

// Frage-Antwort-Paare
const qaPairs = ref([])
const newQuestion = ref('')
const newAnswer = ref('')
const qaTitle = ref('')
const deleteQAPairs = ref([])

// Edit Dialog
const editQADialog = ref(false)
const editQAPairId = ref(null)
const editQATitle = ref('')
const editQAQuestion = ref('')
const editQAAnswer = ref('')

// Edit Dialog für Texte
const editTextDialog = ref(false)
const editTextId = ref(null)
const editTextTitle = ref('')
const editTextContent = ref('')

function startEditText(entry) {
  editTextId.value = entry.id
  editTextTitle.value = entry.title
  editTextContent.value = entry.text
  editTextDialog.value = true
}
function saveEditText() {
  const idx = textEntries.value.findIndex(e => e.id === editTextId.value)
  if (idx !== -1) {
    textEntries.value[idx].title = editTextTitle.value
    textEntries.value[idx].text = editTextContent.value
    localStorage.setItem('knowledgeTexts', JSON.stringify(textEntries.value))
  }
  editTextDialog.value = false
}

function addPair() {
  if (!qaTitle.value.trim() || !newQuestion.value.trim() || !newAnswer.value.trim()) return
  const entry = {
    id: `${qaTitle.value}_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
    title: qaTitle.value,
    question: newQuestion.value,
    answer: newAnswer.value
  }
  qaPairs.value.push(entry)
  localStorage.setItem('qaPairs', JSON.stringify(qaPairs.value))
  qaTitle.value = ''
  newQuestion.value = ''
  newAnswer.value = ''
}
function removeSelectedQAPairs() {
  qaPairs.value = qaPairs.value.filter(entry => !deleteQAPairs.value.includes(entry))
  deleteQAPairs.value = []
  localStorage.setItem('qaPairs', JSON.stringify(qaPairs.value))
}
function startEditQAPair(pair) {
  editQAPairId.value = pair.id
  editQATitle.value = pair.title
  editQAQuestion.value = pair.question
  editQAAnswer.value = pair.answer
  editQADialog.value = true
}
function saveEditQAPair() {
  const idx = qaPairs.value.findIndex(p => p.id === editQAPairId.value)
  if (idx !== -1) {
    qaPairs.value[idx].title = editQATitle.value
    qaPairs.value[idx].question = editQAQuestion.value
    qaPairs.value[idx].answer = editQAAnswer.value
    localStorage.setItem('qaPairs', JSON.stringify(qaPairs.value))
  }
  editQADialog.value = false
}

// Beim Laden aus LocalStorage lesen
if (localStorage.getItem('qaPairs')) {
  qaPairs.value = JSON.parse(localStorage.getItem('qaPairs'))
}

// Speicherplatz-Berechnung
const maxSizeMB = 0.4
const usedSize = computed(() => {
  // Dateien: size in KB, Texte/QA: ggf. size, sonst Textlänge als KB schätzen
  const fileSize = deleteFiles.value.reduce((sum, f) => sum + (f.size || 0), 0)
  const textSize = deleteTexts.value.reduce((sum, t) => sum + (t.size || Math.ceil((t.text?.length || 0)/1024)), 0)
  const qaSize = deleteQAPairs.value.reduce((sum, q) => sum + (q.size || Math.ceil(((q.question?.length||0)+(q.answer?.length||0))/1024)), 0)
  return fileSize + textSize + qaSize
})
const usedSizeMB = computed(() => (usedSize.value/1024).toFixed(2))
const usedPercent = computed(() => Math.min(100, Math.round((usedSize.value/1024)/maxSizeMB*100)))

// Berechnung des belegten Speicherplatzes für die ProgressBar
function updateUsedSize() {
  const totalSize = [...uploadedFiles.value, ...textEntries.value, ...qaPairs.value].reduce((acc, item) => {
    return acc + (item.size || 0)
  }, 0)
  usedSizeMB.value = (totalSize / 1024).toFixed(2) // Umrechnung in MB
  usedPercent.value = (totalSize / (maxSizeMB * 1024)).toFixed(4) * 100
}

// Watcher, um die Größe bei Änderungen zu aktualisieren
watch([uploadedFiles, textEntries, qaPairs], updateUsedSize)

// Zusätzliche Berechnungen für die Gesamtübersicht
const fileSizeAll = computed(() => uploadedFiles.value.reduce((sum, f) => sum + (f.size || 0), 0))
const textSizeAll = computed(() => textEntries.value.reduce((sum, t) => sum + (t.size || Math.ceil((t.text?.length || 0)/1024)), 0))
const qaSizeAll = computed(() => qaPairs.value.reduce((sum, q) => sum + (q.size || Math.ceil(((q.question?.length||0)+(q.answer?.length||0))/1024)), 0))
const usedSizeAll = computed(() => fileSizeAll.value + textSizeAll.value + qaSizeAll.value)
const usedSizeMBAll = computed(() => (usedSizeAll.value/1024).toFixed(2))
const usedPercentAll = computed(() => Math.min(100, Math.round((usedSizeAll.value/1024)/maxSizeMB*100)))

// Training der Wissensbasis
const isTraining = ref(false)
async function trainKnowledgeBase() {
  if (!uploadedFiles.value.length) return
  isTraining.value = true
  try {
    const token = await getAccessTokenSilently({
      audience: import.meta.env.VITE_AUTH0_AUDIENCE,
    })
    if (uploadedFiles.value.length) {
      await indexFilesInVectorDB(uploadedFiles.value, token)
      uploadedFiles.value.forEach(file => {
        file.status = 'Indiziert'
      })
    }
    if (textEntries.value.length) {
      await indexTextsInVectorDB(textEntries.value, token)
    }
    if (qaPairs.value.length) {
      await indexQAPairsInVectorDB(qaPairs.value, token)
    }
    console.log('Wissensbasis wurde erfolgreich indiziert!')
  } catch (err) {
    console.log('Fehler beim Indizieren: ' + err.message)
  } finally {
    isTraining.value = false
  }
}

// Beim Laden der Komponente indizierte Dateien abrufen
onMounted(async () => {
  try {
    const token = await getAccessTokenSilently({
      audience: import.meta.env.VITE_AUTH0_AUDIENCE,
    }).catch(() => null)
    const indexed = await getIndexedFiles(token);
    // Setze Status für bereits indizierte Dateien
    uploadedFiles.value.forEach(file => {
      const found = indexed.find(f => f.title === file.name)
      if (found) file.status = 'Indiziert'
    })
    // Füge indizierte Dateien hinzu, die noch nicht in uploadedFiles sind
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
    })
  } catch (e) {
    // Fehlerbehandlung optional
  }
})
</script>

<style scoped>
/* Nur noch Tailwind, keine Bootstrap- oder Vuetify-Styles */
.files-nav-active {
    background-color: rgb(247, 247, 247);
}
.text-nav-active {
    background-color: rgb(247, 247, 247);
}
.qa-nav-active{
    background-color: rgb(247, 247, 247);
}
.nav-item:hover {
  background-color: rgb(247, 247, 247);
  cursor: pointer;
}
</style>
