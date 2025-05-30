import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'


import { definePreset } from '@primeuix/themes';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
const app = createApp(App)


app.use(createPinia())
app.use(router)

const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{Neutral.50}',
            100: '{Neutral.100}',
            200: '{Neutral.200}',
            300: '{Neutral.300}',
            400: '{Neutral.400}',
            500: '{Neutral.950}',
            600: '{Neutral.600}',
            700: '{Neutral.700}',
            800: '{Neutral.800}',
            900: '{Neutral.900}',
            950: '{Neutral.950}'
        }
    }
});

app.use(PrimeVue, {
  theme: {
  preset: MyPreset,
    options: {
        darkModeSelector: false || 'none',
    }
}
});

import Button from "primevue/button"
import Chart from 'primevue/chart';
app.component('Button', Button);
app.component('Chart', Chart);
app.mount('#app')
