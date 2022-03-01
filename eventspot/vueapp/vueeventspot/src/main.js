import {createApp} from 'vue'
import App from './App.vue'
import router from './routes.js'
import store from './store.js'
import 'bootstrap/dist/css/bootstrap.min.css'

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresLogin)) {
      if (!store.getters.loggedIn) {
        next({ name: 'login' })
      } else {
        next()
      }
    } else {
      next()
    }
  })

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')


