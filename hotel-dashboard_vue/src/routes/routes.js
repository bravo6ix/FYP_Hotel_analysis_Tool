import DashboardLayout from '@/views/Layout/DashboardLayout.vue';
import AuthLayout from '@/views/Pages/AuthLayout.vue';

import NotFound from '@/views/NotFoundPage.vue';

const routes = [
  {
    path: '/',
    redirect: 'dashboard',
    component: DashboardLayout,
    children: [
      {
        path: '/dashboard',
        name: 'dashboard',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "demo" */ '../views/Dashboard.vue')
      },
      {
        path: '/feedback',
        name: 'feedback',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Feedback.vue')
      },
      {
        path: '/hongkongisland',
        name: 'hongkongisland',
        component: () => import(/* webpackChunkName: "demo" */ '../views/HongKongIsland.vue')
      },
      {
        path: '/kowloon',
        name: 'kowloon',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Kowloon.vue')
      },
      {
        path: '/tsimshatsui',
        name: 'tsimshatsui',
        component: () => import(/* webpackChunkName: "demo" */ '../views/TsimShaTsui.vue')
      },
      {
        path: '/yautsimmong',
        name: 'yautsimmong',
        component: () => import(/* webpackChunkName: "demo" */ '../views/YauTsimMong.vue')
      },
      {
        path: '/icons',
        name: 'icons',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Icons.vue')
      },
      {
        path: '/profile',
        name: 'profile',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/UserProfile.vue')
      },
      {
        path: '/maps',
        name: 'maps',
        component: () => import(/* webpackChunkName: "demo" */ '../views/GoogleMaps.vue')
      },
      // {
      //   path: '/tables',
      //   name: 'tables',
      //   component: () => import(/* webpackChunkName: "demo" */ '../views/RegularTables.vue')
      // }
    ]
  },
  {
    path: '/',
    redirect: 'login',
    component: AuthLayout,
    children: [
      {
        path: '/login',
        name: 'login',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/Login.vue')
      },
      {
        path: '/register',
        name: 'register',
        component: () => import(/* webpackChunkName: "demo" */ '../views/Pages/Register.vue')
      },
      { path: '*', component: NotFound }
    ]
  }
];

export default routes;
