import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      children: [
        {
          path: '',
          redirect: '/product'
        },
        {
          path: 'product',
          name: 'productPage',
          component: () => import('../views/ProductView.vue'),
          meta: { title: '产品管理' }
        },
        {
          path: 'esl',
          name: 'eslPage',
          component: () => import('../views/ESLView.vue'),
          meta: { title: '电子标签' }
        },
        {
          path: 'field',
          name: 'fieldPage',
          component: () => import('../views/FieldView.vue'),
          meta: { title: '字段管理' }
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    }
  ]
})

export default router
