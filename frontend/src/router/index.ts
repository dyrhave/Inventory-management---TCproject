import { createRouter, createWebHistory } from 'vue-router'


import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import InventoryView from "@/views/InventoryView.vue";
import CustomerView from "@/views/CustomerView.vue";


const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/inventory',
    name: 'inventory',
    component: InventoryView,
    meta: { requiresAuth: true }
  },
  {
    path: '/customers',
    name: 'customers',
    component: CustomerView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router