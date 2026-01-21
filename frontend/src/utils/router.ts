import { createRouter, createWebHistory} from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

import { useAuthStore } from './auth_store.js';
import HomeView from '/src/views/HomeView.vue';
import LoginView from '/src/views/LoginView.vue'
import RegisterView from '/src/views/RegisterView.vue';
import ScalesView from '/src/views/ScalesView.vue';
import UserMeView from '/src/views/UserMeView.vue';
import ScaleIdView from '/src/views/ScaleIdView.vue';
import CreateScaleView from '/src/views/CreateScaleView.vue';
import NotFound404View from '/src/views/NotFound404View.vue';
import InstrumentScaleView from '/src/views/InstrumentScaleView.vue';



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
    path: '/profile/me/',
    name: 'My Profile',
    component: UserMeView,
    meta: { requiresAuth: true, needsFetch: true }
  },
  {
    path: '/scales/',
    name: 'Public Scales',
    component: ScalesView
  },
  {
    path: '/scales/:scale_id',
    name: 'Scale By ID',
    component: ScaleIdView,
    meta: { needsFetch: true }
  },
  {
    path: '/scales/create',
    name: 'Create Scale',
    component: CreateScaleView,
    meta: { requiresAuth: true, needsFetch: true }
  },
  {
    path: '/instrument/:scale_id',
    name: 'Instrument Scale Representation',
    component: InstrumentScaleView,
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

router.beforeEach(async (to, from, next) => {
  if (to.meta.needsFetch) {
    await useAuthStore().fetchUser();
  }

  useAuthStore().error_message = '';

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
