import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/StorageManager.vue'
import Scanner from '../components/Scanner.vue'
import Add from '../components/Add.vue'
const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/scan',
        name: 'Scanner',
        component: Scanner,
    },
    {
        path: '/add',
        name: 'Add',
        component: Add,
    },
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router