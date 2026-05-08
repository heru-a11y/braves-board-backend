import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import LoginView from '../modules/auth/views/LoginView.vue'
import DashboardView from '../modules/dashboard/views/DashboardView.vue'
import BoardsView from '../modules/board/views/BoardsView.vue'
import BoardsListView from '../modules/board/views/BoardsListView.vue'
import TimeTrackerView from '../modules/timer/views/TimeTrackerView.vue'
import ReportsView from '../modules/reports/views/ReportsView.vue'
import ProjectsView from '../modules/board/views/ProjectsView.vue'
import TeamView from '../modules/team/views/TeamView.vue'

const routes: RouteRecordRaw[] = [
  { path: '/', component: LoginView, meta: { public: true } },
  { path: '/dashboard', component: DashboardView },
  { path: '/boards', component: BoardsListView },
  { path: '/boards/:boardId', component: BoardsView },
  { path: '/tracker', component: TimeTrackerView },
  { path: '/reports', component: ReportsView },
  { path: '/projects', component: ProjectsView },
  { path: '/team', component: TeamView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const params = new URLSearchParams(window.location.search)
  const token = params.get('access_token')

  if (token) {
    localStorage.setItem('access_token', token)
    window.history.replaceState({}, document.title, to.path)
  }

  const isPublic = to.meta.public === true
  const hasToken = !!localStorage.getItem('access_token')

  if (!isPublic && !hasToken) return next('/')
  if (isPublic && hasToken && to.path === '/') return next('/dashboard')

  next()
})

export default router