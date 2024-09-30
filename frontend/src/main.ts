import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import api from './api'


const token = localStorage.getItem('token');
if (token) {
    api.setAuthToken(token);
}

createApp(App).use(store).use(router).mount('#app')
