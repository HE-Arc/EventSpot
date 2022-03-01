import {createRouter, createWebHistory} from 'vue-router'
import Events from './views/Events/Index.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
        path: '/',
        name: 'eventsIndex',
        component: Events,
        },
    ],
})

export default router