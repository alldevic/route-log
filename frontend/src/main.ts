import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import instance from '@/api/Repository';

Vue.config.productionTip = false;

const token = localStorage.getItem('user-token');

if (token) {
  instance.defaults.headers.Authorization = `Token ${token}`;
}

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App),
}).$mount('#app');
