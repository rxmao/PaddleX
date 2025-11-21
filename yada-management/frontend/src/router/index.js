import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/views/Layout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '工作台', icon: 'HomeFilled' }
      },
      {
        path: 'customers',
        name: 'Customers',
        component: () => import('@/views/customer/List.vue'),
        meta: { title: '客户管理', icon: 'UserFilled' }
      },
      {
        path: 'business',
        name: 'Business',
        component: () => import('@/views/business/List.vue'),
        meta: { title: '业务管理', icon: 'DocumentCopy' }
      },
      {
        path: 'finance',
        name: 'Finance',
        component: () => import('@/views/finance/Index.vue'),
        meta: { title: '财务管理', icon: 'Wallet' }
      },
      {
        path: 'employees',
        name: 'Employees',
        component: () => import('@/views/employee/List.vue'),
        meta: { title: '员工管理', icon: 'User' }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('@/views/statistics/Index.vue'),
        meta: { title: '统计分析', icon: 'DataAnalysis' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/Index.vue'),
        meta: { title: '系统设置', icon: 'Setting' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth !== false && !userStore.token) {
    next('/login')
  } else if (to.path === '/login' && userStore.token) {
    next('/')
  } else {
    next()
  }
})

export default router
