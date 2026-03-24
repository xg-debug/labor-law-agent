import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue'), meta: { authPage: true } },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue'), meta: { authPage: true } },
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/consult', name: 'consult', component: () => import('../views/ConsultView.vue') },
  { path: '/contract-review', name: 'contract-review', component: () => import('../views/ContractReviewView.vue') },
  { path: '/document-generate', name: 'document-generate', component: () => import('../views/DocumentGenerateView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('auth_token')
  if (to.meta.authPage && token) return '/'
  return true
})

export default router
