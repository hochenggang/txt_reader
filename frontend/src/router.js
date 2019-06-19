import Vue from 'vue'
import Router from 'vue-router'
import Login from './views/Login.vue'
import All from './views/All.vue'
import Upload from './views/Upload.vue'
import Reader from './views/Reader.vue'
import Signup from './views/Signup.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/all',
      name: 'all',
      component: All
    },
    {
      path: '/upload',
      name: 'upload',
      component: Upload
    },
    {
      path: '/reader',
      name: 'reader',
      component: Reader
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    }
  ]
})
