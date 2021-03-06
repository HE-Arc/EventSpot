import { createStore } from 'vuex'
import { getAPI } from './axios-api'

//store data, token and username
const store = createStore({
  state: {
     accessToken: localStorage.getItem('accessToken'),
     refreshToken: localStorage.getItem('refreshToken'),
     APIData: '',
     username : localStorage.getItem('username')
  },
  mutations: {
    updateStorage (state, { access, refresh, username }) {
      state.accessToken = access
      state.refreshToken = refresh
      state.username = username

      //set data to localstorage
      localStorage.setItem('accessToken', access)
      localStorage.setItem('refreshToken', refresh)
      localStorage.setItem('username', username)

    },
    destroyToken (state) {
      state.accessToken = null
      state.refreshToken = null
      state.username = null

      //remove data to localstorage
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('username')
    }
  },
  getters: {
    loggedIn (state) {
      return state.accessToken != null
    }
  },
  actions: {
    userLogout (context) {
      if (context.getters.loggedIn) {
          context.commit('destroyToken')
      }
    },
    userLogin (context, usercredentials) {
      return new Promise((resolve, reject) => {
        getAPI.post('/token/', {
          username: usercredentials.username.toLowerCase(),
          password: usercredentials.password
        })
          .then(response => {
            context.commit('updateStorage', { access: response.data.access, refresh: response.data.refresh, username:usercredentials.username }) 
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    }
  }
})

export default store