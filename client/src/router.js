import Vue from 'vue';
import Router from 'vue-router';
import Books from './components/Books.vue';
import Cam from './components/Cam.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: '/soli/',
  routes: [
    {
      path: '/',
      name: 'Cam',
      component: Cam,
    },
    {
      path: '/books',
      name: 'Books',
      component: Books,
    },
  ],
});
