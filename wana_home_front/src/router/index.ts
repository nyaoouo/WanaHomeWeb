import Vue from 'vue'
import VueRouter, {RouteConfig} from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
    {
        path: '/',
        name: 'ServerList',
        component: () => import(/* webpackChunkName: "about" */ '../views/ServerList.vue')
    },
    {
        path: '/captcha',
        name: 'Captcha',
        component: () => import(/* webpackChunkName: "about" */ '../views/Recaptcha.vue')
    },
    {
        path: '/state/:server',
        name: 'State',
        component: () => import(/* webpackChunkName: "about" */ '../views/ServerState.vue')
    },
    {
        path: '/state/:server/:map',
        name: 'ServerMap',
        component: () => import(/* webpackChunkName: "about" */ '../views/ServerMap.vue')
    },
    {
        path: '/ngld',
        name: 'Ngld',
        component: () => import(/* webpackChunkName: "about" */ '../views/Ngld.vue')
    },
    {
        path: "*",
        redirect: {name: 'ServerList'},
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
