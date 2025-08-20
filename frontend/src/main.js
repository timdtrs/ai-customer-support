import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'


import { definePreset } from '@primeuix/themes';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
const app = createApp(App)

import { createAuth0 } from '@auth0/auth0-vue';

app.use(createPinia())

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

// Install Auth0 before router so guards can access it
app.use(
  createAuth0({
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
    authorizationParams: {
      redirect_uri: window.location.origin,
      audience: import.meta.env.VITE_AUTH0_AUDIENCE,
    },
    cacheLocation: 'localstorage',
    useRefreshTokens: true,
  })
);

app.use(router)

import Button from "primevue/button"
import Chart from 'primevue/chart';
app.component('Button', Button);
app.component('Chart', Chart);
app.mount('#app')
