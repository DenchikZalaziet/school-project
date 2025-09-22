import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

import { useAuthStore } from './auth_store';
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue';
import ScalesView from '@/views/ScalesView.vue';
import UserMeView from '@/views/UserMeView.vue';
import ScaleIdView from '@/views/ScaleIdView.vue';
import CreateScaleView from '@/views/CreateScaleView.vue';
import NotFound404View from '@/views/NotFound404View.vue';



const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  },
  {
    path: '/profile/me',
    name: 'My Profile',
    component: UserMeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/scales',
    name: 'Public Scales',
    component: ScalesView
  },
  {
    path: '/scales/:scale_id',
    name: 'Scale By ID',
    component: ScaleIdView,
  },
  {
    path: '/scales/create',
    name: 'Create Scale',
    component: CreateScaleView,
    meta: { requiresAuth: true }
  },

  // 404
  {
    path: '/:pathMatch(.*)*',
    name: '404',
    component: NotFound404View
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const isLoggedIn = useAuthStore().isAuthenticated;
    
    if (isLoggedIn) {
      next();
    } else {
      next({ name: 'Login' });
    };
  } else {
    next();
  };
});

export default router;
