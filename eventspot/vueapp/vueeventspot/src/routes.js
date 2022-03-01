import {createRouter, createWebHistory} from 'vue-router'
import Events from './views/Events/Index.vue'
import Login from './views/Login.vue'
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
        path: '/logout',
        name: 'logout',
        component: Logout,
        },
    ],
})

export default router