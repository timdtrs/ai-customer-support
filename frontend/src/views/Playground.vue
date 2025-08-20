<template>
  <div class="flex flex-col p-8 h-full">
    <h1 class="text-3xl font-bold mb-2">Playground</h1>
    <span class="text-gray-500 mb-6">Konfiguriere und teste deinen Chatbot</span>
    <div class="flex flex-row gap-8 w-full h-full">
      <div class="w-full lg:w-2/4 2xl:w-1/4 flex flex-col gap-8">
        <TabMenu :model="tabMenuItems" :activeIndex="activeTabIndex" @tab-change="onTabChange" />
        <router-view />
      </div>
      <div class="w-full lg:w-1/2 2xl:w-3/4 flex flex-col items-center">
        <!-- Chat bleibt immer sichtbar -->
        <div class="flex flex-col bg-white rounded-xl w-full max-w-2xl h-full 2xl:h-4/5">
          <h4 class="block font-semibold text-gray-500 mb-1">Teste deinen Chatbot</h4>
          <div class="flex flex-col flex-grow rounded-2xl p-4 bg-gray-100 overflow-auto">
            <div class="flex-grow mb-3 overflow-auto" ref="messagesEnd">
              <div v-for="(msg, idx) in messages" :key="idx"
                   class="mb-2 flex w-full"
                   :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
                <div class="flex items-center gap-2 w-fit max-w-[70%]"
                     :class="msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'">
                  <i v-if="msg.role === 'user'" class="pi pi-user text-xl"></i>
                  <i v-else class="pi pi-android text-xl"></i>
                  <div :class="[
                    'px-3 py-2 rounded-lg',
                    msg.role === 'user' ? 'bg-blue-100 text-blue-900 self-end' : 'bg-gray-700 text-white self-start'
                  ]">
                    <span v-if="msg.role === 'user'">{{ msg.content }}</span>
                    <Markdown v-else :source="msg.content.replace(/\n/g, '\n')" />
                  </div>
                </div>
              </div>
            </div>
            <form class="flex gap-2 mt-auto" @submit.prevent="sendMessage">
              <InputText v-model="input" type="text" class="flex-grow" placeholder="Nachricht an den Chatbot..." autocomplete="off" />
              <Button icon="pi pi-send" class="flex items-center justify-center w-10 h-10 rounded-full" type="submit" />
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, provide } from 'vue'
import TabMenu from 'primevue/tabmenu'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { useRouter, useRoute } from 'vue-router'
import Markdown from 'vue3-markdown-it'
import { useAuth0 } from '@auth0/auth0-vue'

const router = useRouter()
const route = useRoute()
const { getAccessTokenSilently } = useAuth0()

const tabMenuItems = [
  { label: 'Konfigurieren', icon: 'pi pi-cog', to: '/playground/config' },
  { label: 'Exportieren', icon: 'pi pi-external-link', to: '/playground/export' }
]
const tabRoutes = ['/playground/config', '/playground/export']
const activeTabIndex = ref(tabRoutes.indexOf(route.path) !== -1 ? tabRoutes.indexOf(route.path) : 0)

function onTabChange(e) {
  activeTabIndex.value = e.index
  router.push(tabRoutes[e.index])
}

// States für provide/inject
const modelOptions = [
  { label: 'GPT-3.5 Turbo', value: 'gpt-3.5-turbo' },
  { label: 'GPT-4', value: 'gpt-4' },
  { label: 'GPT-4o', value: 'gpt-4o' }
]
const selectedModel = ref(modelOptions[0].value)
const temperature = ref(0.7)
const systemMessage = ref('')
const agentId = "test"


provide('selectedModel', selectedModel)
provide('modelOptions', modelOptions)
provide('temperature', temperature)
provide('systemMessage', systemMessage)
provide('agentId', agentId)


// Chatverlauf
const messages = ref([
  { role: 'assistant', content: 'Hallo! Wie kann ich dir helfen?' }
])
const input = ref('')
const messagesEnd = ref(null)

async function sendMessage() {
  if (!input.value.trim()) return
  messages.value.push({ role: 'user', content: input.value })
  const assistantMsg = { role: 'assistant', content: '' }
  messages.value.push(assistantMsg)
  try {
    const token = await getAccessTokenSilently({
      audience: import.meta.env.VITE_AUTH0_AUDIENCE,
      ignoreCache: true
    });
    console.log("Token:", token);
    await (await import('@/api/generate')).generateAnswer(
      { query: input.value, messages: messages.value, agent_id: "Test" },
      token,
      (chunk) => {
        assistantMsg.content += chunk
        messages.value = [...messages.value] // Trigger reactivity
        scrollToEnd()
      }
    )
  } catch (e) {
    assistantMsg.content = 'Fehler bei der Anfrage.'
  }
  input.value = ''
  scrollToEnd()
}
function scrollToEnd() {
  nextTick(() => {
    if (messagesEnd.value) messagesEnd.value.scrollTop = messagesEnd.value.scrollHeight
  })
}
</script>
