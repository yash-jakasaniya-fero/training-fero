import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify

import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'


const app = createApp(App)

const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',  
  },
  components,
  directives,
})


app.use(router)
app.use(vuetify)

app.mount('#app')
