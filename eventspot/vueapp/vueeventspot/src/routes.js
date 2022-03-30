import {createRouter, createWebHistory} from 'vue-router'
import Events from './views/Events/Index.vue'
import Friends from './views/Friends/Index.vue'
import EventsShow from './views/Events/Show.vue'
import EventsCreate from './views/Events/Create.vue'
import EventsUpdate from './views/Events/Create.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Profile from './views/Profile.vue'
import Logout from './views/Logout.vue'
import NotFoundPage from './components/NotFoundPage.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
        path: '/events/:state?',
        name: 'events',
        component: Events,
        meta: {
            },
        },
        { 
        path: '/events/create', 
        name: 'events.create',
        component: EventsCreate,
        meta: {
                requiresLogin: true
            } 
        },
        { 
        path: '/events/:id/:state?', 
        name: 'events.show',
        component: EventsShow,
        meta: {
                requiresLogin: true
            } 
        },

        { 
        path: '/events/:id/update', 
        name: 'events.update',
        component: EventsUpdate,
        meta: {
                requiresLogin: true
            } 
        },

        {
        path: '/friends',
        name: 'friends',
        component: Friends,
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
        { 
            path: '/:pathMatch(.*)*',
            name: 'notFoundPage',
            component: NotFoundPage 
        },
       
    ],
})

export default router