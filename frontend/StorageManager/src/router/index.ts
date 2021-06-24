import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/StorageManager.vue'
import Scanner from '../components/Scanner.vue'
import AddItem from '../components/AddItem.vue'
import AddCategory from '../components/AddCategory.vue'
import Overview from '../components/Overview.vue'
import ItemDetail from '../components/ItemDetail.vue'
const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/overview',
        name: 'Overview',
        component: Overview
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
        path: '/itemdetail',
        name: 'ItemDetail',
        component: ItemDetail,
        props: true
    },
    {
        path: '/addcategory',
        name: 'AddCategory',
        component: AddCategory
    },

]
const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router