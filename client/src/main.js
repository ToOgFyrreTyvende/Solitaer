import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue-icons.min.css'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import VueTour from 'vue-tour'
require('vue-tour/dist/vue-tour.css')

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons)
Vue.use(VueTour)

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
