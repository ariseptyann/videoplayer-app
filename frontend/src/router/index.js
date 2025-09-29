import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Video from '../pages/Video.vue'
import Qr from '../pages/Qr.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/video',
            name: 'video',
            component: Video
        },
        {
            path: '/qr',
            name: 'qr',
            component: Qr
        }
    ]
})

export default router