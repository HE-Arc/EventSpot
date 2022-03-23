import {createRouter, createWebHistory} from 'vue-router'
import Events from './views/Events/Index.vue'
import EventsShow from './views/Events/Show.vue'
import EventsCreate from './views/Events/Create.vue'
import EventsUpdate from './views/Events/Create.vue'

import Login from './views/Login.vue'
import Logout from './views/Logout.vue'
import NotFoundPage from './components/NotFoundPage.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
        path: '/:state?',
        name: 'eventsIndex',
        component: Events,
        meta: {
                requiresLogin: true
            }
        },

        { 
        path: '/events/:id/:state?', 
        name: 'eventsShow',
        component: EventsShow,
        meta: {
                requiresLogin: true
            } 
        },

        { 
            path: '/events/create', 
            name: 'eventsCreate',
            component: EventsCreate,
            meta: {
                    requiresLogin: true
                } 
        },

        { 
            path: '/events/:id/update', 
            name: 'eventsUpdate',
            component: EventsUpdate,
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
        { 
            path: '/:pathMatch(.*)*',
            name: 'notFoundPage',
            component: NotFoundPage 
        },

       
    ],
})

export default router