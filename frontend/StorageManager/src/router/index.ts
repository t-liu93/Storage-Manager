import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/StorageManager.vue'
import Scanner from '../components/Scanner.vue'
import AddItem from '../components/AddItem.vue'
import AddCategory from '../components/AddCategory.vue'
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
        path: '/additem',
        name: 'AddItem',
        component: AddItem,
    },
    {
        path: '/addcategory',
        name: 'AddCategory',
        component: AddCategory
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router