import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'


const routes = [
  {
    name: 'admin',
    path: '/',
    component: DefaultLayout,
    redirect: { name: 'users' },
    children: [
      {
        path: '/users',
        name: 'users',
        component: () => import('../views/Userlist.vue')
      },
    ]
  },
  {
    name: 'login',
    path: '/login',
    component: () => import('../views/pages/LoginView.vue')
  },
  {
    name: 'recover-password',
    path: '/recover-password',
    component: () => import('../views/pages/LoginView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router
