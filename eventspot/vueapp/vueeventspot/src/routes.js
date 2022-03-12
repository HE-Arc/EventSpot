import {createRouter, createWebHistory} from 'vue-router'
import Events from './views/Events/Index.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Profile from './views/Profile.vue'
import Logout from './views/Logout.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
        path: '/',
        name: 'eventsIndex',
        component: Events,
        meta: {
                requiresLogin: true
            }
        },

        {
        path: '/login',
        name: 'login',
        component: Login,
        },

        {
        path: '/register',
        name: 'register',
        component: Register,
        },

        {
        path: '/logout',
        name: 'logout',
        component: Logout,
        },

        {
        path: '/profile',
        name: 'profilePage',
        component: Profile,
        meta: {
                requiresLogin: true
            }
        },
    ],
})

export default router