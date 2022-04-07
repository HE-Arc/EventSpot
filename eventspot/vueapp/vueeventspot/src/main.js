import {createApp} from 'vue'
import App from './App.vue'
import router from './routes.js'
import store from './store.js'
import { getAPI, getAPIAuth } from './axios-api'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import moment from 'moment';


library.add(fas);
import { dom } from "@fortawesome/fontawesome-svg-core";
dom.watch();

//check if login is required
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

//refresh token when a new request to the service rest is done
getAPI.interceptors.request.use(request => {
    
  if(store.state.refreshToken != undefined) {
      const data = {
          refresh: store.state.refreshToken
      }

      getAPIAuth.post('/token/refresh/', data)
      .then(response => {
          store.state.accessToken = response.data.access;
      })
    }

    return request;
});

const app = createApp(App)

app.config.globalProperties.$moment=moment;


app.use(router)
app.use(store)
app.use(moment)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')




