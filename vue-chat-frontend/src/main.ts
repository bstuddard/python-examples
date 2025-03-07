// Library
import { createApp } from 'vue';

// Types
import type { App as AppInstance } from 'vue';

// Local files
import App from './App.vue';
import router from './router';
import './assets/css/main.css';


// Create/route/mount app
const app: AppInstance = createApp(App);
app.use(router)
app.mount('#app')
