import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import instance from '@/api/Repository';
import dateBeautify from '@/filters/DateFilter'

Vue.config.productionTip = false;

const token = localStorage.getItem('user-token');

if (token) {
  instance.defaults.headers.Authorization = `Token ${token}`;
}

Vue.filter('date', dateBeautify)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App),
}).$mount('#app');
