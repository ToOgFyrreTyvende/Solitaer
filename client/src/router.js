import Vue from 'vue';
import Router from 'vue-router';
import Cam from './components/Cam.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      name: 'Cam',
      component: Cam,
    }
  ],
});
