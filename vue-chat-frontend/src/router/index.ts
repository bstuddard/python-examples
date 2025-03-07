// Library
import { createRouter, createWebHistory } from 'vue-router';

// Types
import type { RouteRecordRaw, Router } from 'vue-router';

// Local files
// import HomePage from '@/views/HomePage.vue';
import PageNotFound from '@/views/PageNotFound.vue';
import ChatPage from '@/views/ChatPage.vue';
import { devlog } from '@/devlogger/devlogger';

// Build various paths using router
const routes: Array<RouteRecordRaw> = [
  {
      path: '/',
      name: 'HomePage',
      component: ChatPage
  },
  {
      path: '/home',
      name: 'Home',
      component: ChatPage
  },
  // Catch all for 404 Not Found
  {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: PageNotFound
  }
]

// Extend default router to capture web history
const router: Router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  devlog('Running router before.')
  next();
});

export default router;