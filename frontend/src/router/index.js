import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/consult', name: 'consult', component: () => import('../views/ConsultView.vue') },
  { path: '/contract-review', name: 'contract-review', component: () => import('../views/ContractReviewView.vue') },
  { path: '/document-generate', name: 'document-generate', component: () => import('../views/DocumentGenerateView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
