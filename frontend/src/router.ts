import Vue from 'vue';
import Router from 'vue-router';
import Login from '@/views/authorization/Login.vue';
import ShippingReportList from '@/views/shipping-report/List.vue';
// import ShippingReportDetail from '@/views/shipping-report/Detail.vue';
import store from '@/store';

Vue.use(Router);

const ifNotAuthenticated = (to: any, from: any, next: any) => {
  if (!store.getters.isAuthenticated) {
    next();
  } else {
    next('/');
  }
};

const ifAuthenticated = (to: any, from: any, next: any) => {
  if (store.getters.isAuthenticated) {
    next();
  } else {
    next('/login/');
  }
};

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: '/shipping-report-list/',
    },
    {
      path: '/login',
      name: 'login',
      props: { appBar: false, navigationDrawer: false },
      component: Login,
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/shipping-report-list/',
      name: 'shipping-report-list',
      component: ShippingReportList,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/shipping-report-detail/:id/',
      name: 'shipping-report-detail',
      component: () => import('@/views/shipping-report/Detail.vue'),
      beforeEnter: ifAuthenticated,
    },
  ],
});
